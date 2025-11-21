## Bare linux process
My vLLM version:
```console
$ vllm --version
INFO 11-14 17:22:53 [__init__.py:241] Automatically detected platform cuda.
0.10.1.dev544+gc90fb03df.precompiled
```

I started both of the ranks as follows.
```shell
# Rank 0 in one terminal
MODEL=ibm-granite/granite-3.3-8b-instruct
CUDA_VISIBLE_DEVICES=0 vllm serve $MODEL --data-parallel-size 2 --data-parallel-rank 0 --port 8000 --max-model-len 8192
# Rank 1 in another terminal
MODEL=ibm-granite/granite-3.3-8b-instruct
CUDA_VISIBLE_DEVICES=1 vllm serve $MODEL --data-parallel-size 2 --data-parallel-rank 1 --port 8001 --max-model-len 8192
```
Here 'rank' is the index of a replica in vLLM data-parallel deployment.

I checked the GPU memory usage.
```console
$ nvidia-smi --query-gpu=index,uuid,memory.used,memory.total --format=csv
index, uuid, memory.used [MiB], memory.total [MiB]
0, GPU-2762b558-7fac-024b-2b6f-209a2e06b94c, 21246 MiB, 23034 MiB
1, GPU-5401efac-69f8-97a4-8127-ca26c1b9f6b6, 21246 MiB, 23034 MiB
2, GPU-e3386481-63c3-aa75-3b61-363533329fa5, 0 MiB, 23034 MiB
3, GPU-25ea96f1-02f7-7251-d394-3d34f29939ee, 0 MiB, 23034 MiB
```

I sent inference requests as follows.
```shell
curl -s localhost:8000/v1/completions -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.3-8b-instruct",
        "prompt": "The capital of the US is ",
        "max_tokens": 20
      }' | jq

curl -s localhost:8001/v1/completions -H "Content-Type: application/json" \
  -d '{
        "model": "ibm-granite/granite-3.3-8b-instruct",
        "prompt": "The capital of the US is ",
        "max_tokens": 20
      }' | jq
```


### Observation and Question
The log from rank 0 has such a line:
```text
(APIServer pid=13926) INFO 11-14 17:03:51 [utils.py:625] Started DP Coordinator process (PID: 14168)
```
The log from rank 1 doesn't have such a line.
This is also true if I first start rank 1 then start rank 0: Rank 0 is in charge of starting the 'coordinator process'.

Rank 0 will be 'Waiting for init message from front-end' as follows:
```text
(EngineCore_0 pid=14171) INFO 11-14 17:03:56 [core.py:619] Waiting for init message from front-end.
(EngineCore_0 pid=14171) INFO 11-14 17:06:45 [core.py:72] Initializing a V1 LLM engine (v0.10.1.dev544+gc90fb03df)...
```
The log shows that rank 0 waited for roughly 3 minutes, until I started rank 1.
This is similar if I first start rank 1 then start rank 0: Rank 1 waits for rank 0 as well.

The question is, how could the 'coordinator process' coordinate two ranks on Kubernetes?
Maybe the two ranks must be collocated within one pod.


## Using Kubernetes
```shell
kubectl create -f ./vllm-data-parallelism/deployment.yaml
```

Check the log of the two ranks:
```shell
kubectl logs deploy/vllm-dp -c rank0 -f
kubectl logs deploy/vllm-dp -c rank1 -f
```


## References
- [vLLM doc on 'External Load Balancing'](https://docs.vllm.ai/en/latest/serving/data_parallel_deployment/#external-load-balancing)
- [Support for vLLM Data parallel](https://github.com/kubernetes-sigs/gateway-api-inference-extension/pull/1663)
