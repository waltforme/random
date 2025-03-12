An experiment attempting to make two vLLM instances cosleep on one GPU

### Setup
- AWS EC2 g6.4xlarge instance (one NVIDIA L4 GPU with 24GB GPU memory)
- Kubernetes v1.32.2 bootstrapped by kubeadm
- vLLM v0.7.3

### Two bare processes

Two vLLM instances can cosleep on the GPU.
They can't be both awake on one GPU. I got
```text
ERROR 03-11 17:23:51 [core.py:305]     raise ValueError("No available memory for the cache blocks. "
ERROR 03-11 17:23:51 [core.py:305] ValueError: No available memory for the cache blocks. Try increasing `gpu_memory_utilization` when initializing the engine.
```
when I tried that without specifying the `--gpu-memory-utilization` flag.

#### Commands

First vLLM instance.
```shell
date; VLLM_USE_V1=1 VLLM_SERVER_DEV_MODE=1 vllm serve openai-community/gpt2 --enable-sleep-mode --port 8001
```

Second vLLM intance.
```shell
date; VLLM_USE_V1=1 VLLM_SERVER_DEV_MODE=1 vllm serve openai-community/gpt2 --enable-sleep-mode --port 8002
```

An additional terminal to control the two vLLM instances.
```shell
# start the 1st instance
curl -X POST localhost:8001/sleep
# start the 2nd instance
curl -X POST localhost:8002/sleep

curl -X POST localhost:8001/wake_up # succeeded
curl -s localhost:8001/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "openai-community/gpt2",
        "prompt": "IBM is a",
        "max_tokens": 20

      }' | jq
curl -X POST localhost:8001/sleep

curl -X POST localhost:8002/wake_up # succeeded
curl -s localhost:8002/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "openai-community/gpt2",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
curl -X POST localhost:8002/sleep

nvidia-smi # 968MiB in use
kill 488147
nvidia-smi # 487MiB in use
kill 489275
nvidia-smi # 1MiB in use
```

### Two bare processes with `--gpu_memory_utilization` flag

Two vLLM instances can cosleep on the GPU.
They can be both awake on one GPU, with `--gpu_memory_utilization 0.4`.

#### Commands

First vLLM instance.
```
date; VLLM_USE_V1=1 VLLM_SERVER_DEV_MODE=1 vllm serve ibm-granite/granite-3.2-2b-instruct --max-model-len 1024 --gpu_memory_utilization 1.0 --enable-sleep-mode --port 8001
```

Second vLLM instance.
```
date; VLLM_USE_V1=1 VLLM_SERVER_DEV_MODE=1 vllm serve ibm-granite/granite-3.2-2b-instruct --max-model-len 1024 --gpu_memory_utilization 1.0 --enable-sleep-mode --port 8002
```

An additional terminal to control the two vLLM instances.
```shell
# start the 1st instance
curl -X POST localhost:8001/sleep
# start the 2nd instance
curl -X POST localhost:8002/sleep

curl -X POST localhost:8001/wake_up # succeeded
curl -s localhost:8001/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.2-2b-instruct",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
curl -X POST localhost:8001/sleep

curl -X POST localhost:8002/wake_up # succeeded
curl -s localhost:8002/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.2-2b-instruct",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
curl -X POST localhost:8002/sleep

curl -X POST localhost:8001/wake_up # succeeded
curl -X POST localhost:8002/wake_up # succeeded
curl -s localhost:8001/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.2-2b-instruct",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
curl -s localhost:8002/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.2-2b-instruct",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq

nvidia-smi # 14036MiB /  23034MiB
curl -X POST localhost:8001/sleep
nvidia-smi # 7454MiB /  23034MiB
curl -X POST localhost:8002/sleep
nvidia-smi 1752MiB /  23034MiB
kill 495224
nvidia-smi # 881MiB /  23034MiB
kill 495938
nvidia-smi # 1MiB /  23034MiB
```

### One Kubernetes Deployment and one bare process

If the Deployment is awake and I try to wake up the sleeping bare process, I get
```text
Exception: Call to wake_up method failed: CUDA Error: out of memory at /workspace/csrc/cumem_allocator.cpp:62
```
At this time I put the Deployment to sleep and try again to wake up the bare process, I get
```text
Exception: Call to wake_up method failed: CUDA Error: invalid argument at /workspace/csrc/cumem_allocator.cpp:66
```
At this time I wake up the Deployment.
The Deployment can serve requests successfully.
At this time I kill the Deployment and try the 3rd time to wake up the bare process, I still get
```
Exception: Call to wake_up method failed: CUDA Error: invalid argument at /workspace/csrc/cumem_allocator.cpp:66
```
So looks like failure to wake up is permanent.

Same two errors show up when I do the opposite, i.e. the bare process is initially awake and I try thrice to wake up the sleeping Deployment.
So conclusion is that one bare process and one Kubernetes Deployment can't be both awake on one GPU.
I wonder what would happen if the models are small enough. In other words, is size the only constraint?

### Two Kubernetes Deployments

If the 1st Deployment exists, even asleep, then the 2nd Deployment can't be scheduled. I get
```text
1m38s       Warning   FailedScheduling   Pod/gpt2-5965c886db-vj847   0/1 nodes are available: 1 Insufficient nvidia.com/gpu. preemption: 0/1 nodes are available: 1 No preemption victims found for incoming pod.
```
So conclusion is that two vLLM Kubernetes Deployments can't simultaneously use one GPU.
At lease in the absence of any GPU sharing technologies.

### Commands for bare process

```shell
date; VLLM_USE_V1=1 VLLM_LOGGING_LEVEL=DEBUG VLLM_SERVER_DEV_MODE=1 vllm serve openai-community/gpt2 --enable-sleep-mode --enforce-eager
curl -s localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "openai-community/gpt2",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
```

### Commands for Kubernetes

Commands for the 1st Deployment.
```shell
kubectl apply -f vllm-cosleep/deployment_gpt2.yaml
kubectl apply -f vllm-cosleep/service_gpt2.yaml
kubectl logs deploy/gpt2 -f
curl -s localhost:30081/v1/models | jq # have to wait for a few seconds, why?
curl -X POST localhost:30081/sleep
curl -X POST localhost:30081/wake_up
kubectl delete -f vllm-cosleep/deployment_gpt2.yaml
curl -s localhost:30081/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "openai-community/gpt2",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
```

Commands for the 2nd Deployment.
```shell
kubectl apply -f vllm-cosleep/deployment_gpt2-pmc.yaml
kubectl apply -f vllm-cosleep/service_gpt2-pmc.yaml
kubectl logs deploy/gpt2-pmc -f
curl -s localhost:30082/v1/models | jq
curl -X POST localhost:30082/sleep
curl -X POST localhost:30082/wake_up
kubectl delete -f vllm-cosleep/deployment_gpt2-pmc.yaml
curl -s localhost:30082/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
        "model": "manupande21/GPT2_PMC",
        "prompt": "IBM is a",
        "max_tokens": 20
      }' | jq
```
