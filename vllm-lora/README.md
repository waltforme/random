Getting hands on LoRA adapters with vLLM.

### Overview
```txt
┌────────────────────────────────────────────────────────────────────┐
│                                                                    │
│   ┌────────────────────────────┐  ┌────────────────────────────┐   │
│   │┌──────────────────────────┐│  │┌──────────────────────────┐│   │
│   ││ Qwen/Qwen2-0.5B-Instruct ││  ││ Qwen/Qwen2-0.5B-Instruct ││   │
│   ││──────────────────────────││  ││──────────────────────────││   │
│   ││           vLLM           ││  ││           vLLM           ││   │
│   │└──────────────────────────┘│  │└──────────────────────────┘│   │
│   │         Deployment         │  │         Deployment         │   │
│   └────────────────────────────┘  └────────────────────────────┘   │
│                  │                               │                 │
│                  │             read              │                 │
│                  └───────────────┬───────────────┘                 │
│                                  │                                 │
│                                  │                                 │
│                        ┌─────────┼─────────┐                       │
│                        │         │         │                       │
│                        │  ┌──────▼──────┐  │                       │
│                        │  │LoRA adapters│  │                       │
│                        │  └─────────────┘  │                       │
│                        │        PV         │                       │
│                        └───────────────────┘                       │
│                                                                    │
│                                                                    │
│                              Kubernetes                            │
└────────────────────────────────────────────────────────────────────┘
```

### Steps
A [kind](https://kind.sigs.k8s.io/) cluster is used in this experiment.
```shell
kind --version # kind version 0.26.0
kind create cluster --config=./vllm-lora/kind/cluster_lora.yaml
```

A docker container image has the logic to download LoRA adapters from Hugging Face.
Build the image and load it into the kind cluster.
```shell
pushd ./vllm-lora/preparer
docker build -t myrepo/prepare-adapters:latest .
kind load --name lora docker-image myrepo/prepare-adapters:latest
docker exec lora-control-plane crictl images
popd
```

A Kubernetes Job runs the container, saving the downloaded LoRA adapters to a Kubernetes PV.
```shell
kubectl apply -f ./vllm-lora/pvc_shared-adapters.yaml
kubectl apply -f ./vllm-lora/job_prepare-adapters.yaml
kubectl logs job/prepare-adapters # "All adapters downloaded successfully."
```

CPUs (instead of GPUs) are used in this experiment.
To use CPUs, use vLLM-offered `Dockerfile.cpu` to build a container image.
Load the image into the kind cluster.
```shell
# Build in the root dir of the git-cloned https://github.com/vllm-project/vllm.git.
# This experiment uses commit dd6a3a02cb3bf2a7bc6cb84c85dcd57c6eaf2bf9.
docker build -f Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
kind load --name lora docker-image vllm-cpu-env:latest
docker exec lora-control-plane crictl images
```

Run the 1st vLLM instance by a Kubernetes Deployment,
then expose the Deployment via a Service.
```shell
kubectl apply -f ./vllm-lora/deployment_qwen2.yaml
kubectl wait --for=condition=Available deployment/qwen2 --timeout=300s
kubectl apply -f ./vllm-lora/service_qwen2.yaml
```

Unload/Load LoRA adapters.
Note that loading an adapter is indeed much faster than loading the model that the adapter is based on.
```shell
curl -s http://localhost:30080/v1/models | jq # two items, base model plus lora adapter "ru-lora"
curl -s http://localhost:30080/v1/models | jq .data[0].id # "Qwen/Qwen2-0.5B-Instruct"
curl -s http://localhost:30080/v1/models | jq .data[1].id # "ru-lora"

# unload the ru-lora adapter
curl -s http://localhost:30080/v1/models | jq .data[1].id
curl -X POST http://localhost:30080/v1/unload_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "ru-lora"
}'
curl -s http://localhost:30080/v1/models | jq .data[1].id # null

# (re)load the ru-lora adapter
curl -s http://localhost:30080/v1/models | jq .data[1].id # null
curl -X POST http://localhost:30080/v1/load_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "ru-lora",
    "lora_path": "/data/qwen2-ru-lora"
}'
curl -s http://localhost:30080/v1/models | jq .data[1].id
```

Inference.
```shell
# inference by Qwen2-0.5B-Instruct
curl -s http://localhost:30080/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2-0.5B-Instruct",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq .choices[0].text

# inference by Qwen2-0.5B-Instruct+ru-lora
curl -s http://localhost:30080/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ru-lora",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq .choices[0].text
```

Take simlar steps to run the 2nd vLLM instance.
```shell
kubectl apply -f ./vllm-lora/deployment_qwen2-copy.yaml
kubectl wait --for=condition=Available deployment/qwen2-copy --timeout=300s
kubectl apply -f ./vllm-lora/service_qwen2-copy.yaml
```

Load/Unload LoRA adapters, and inference.
```shell
curl -s http://localhost:30081/v1/models | jq # two items, base model plus lora adapter "code-lora"

# inference by Qwen2-0.5B-Instruct
curl -s http://localhost:30081/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "Qwen/Qwen2-0.5B-Instruct",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq .choices[0].text

# inference by Qwen2-0.5B-Instruct+code-lora
curl -s http://localhost:30081/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "code-lora",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq .choices[0].text

# load the ru-lora adapter
curl -s http://localhost:30081/v1/models | jq .data[2].id # null
curl -X POST http://localhost:30081/v1/load_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "ru-lora",
    "lora_path": "/data/qwen2-ru-lora"
}'
curl -s http://localhost:30081/v1/models | jq # three items, base model plus lora adapters "code-lora" and "ru-lora"
curl -s http://localhost:30081/v1/models | jq .data[2].id

# inference by Qwen2-0.5B-Instruct+ru-lora
curl -s http://localhost:30081/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "ru-lora",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq .choices[0].text

# unload the ru-lora adapter
curl -s http://localhost:30081/v1/models | jq .data[2].id
curl -X POST http://localhost:30081/v1/unload_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "ru-lora"
}'
curl -s http://localhost:30081/v1/models | jq .data[2].id # null

# cleaning up workloads from the cluster
kubectl delete -f ./vllm-lora/

# tearing down the cluster
kind delete cluster --name lora
```

### Local Python Run without Kubernetes
LoRA adapters can be statically loaded at the beginning, or dynamically loaded/unloaded at runtime.
As long as files for the adapters are saved somewhere before hand.

Statically loaded at the beginning.
```shell
vllm serve Qwen/Qwen2-0.5B-Instruct \
    --enable-lora \
    --lora-modules some-lora=$HOME/.cache/huggingface/hub/models--sikoraaxd--Qwen2-0.5B-Instruct-ru-lora/snapshots/f1fa56303ae329d2c19f61e2fd51a82c48e32003/
# alternatively
python3 -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2-0.5B-Instruct \
    --enable-lora \
    --lora-modules some-lora=$HOME/.cache/huggingface/hub/models--sikoraaxd--Qwen2-0.5B-Instruct-ru-lora/snapshots/f1fa56303ae329d2c19f61e2fd51a82c48e32003/
```

Dynamically loaded/unloaded at runtime.
```shell
VLLM_ALLOW_RUNTIME_LORA_UPDATING=True vllm serve Qwen/Qwen2-0.5B-Instruct --enable-lora
curl -s http://localhost:8000/v1/models | jq .data[0].id
curl -X POST http://localhost:8000/v1/load_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "some-lora",
    "lora_path": "/home/ubuntu/.cache/huggingface/hub/models--sikoraaxd--Qwen2-0.5B-Instruct-ru-lora/snapshots/f1fa56303ae329d2c19f61e2fd51a82c48e32003/"
}'
curl -s http://localhost:8000/v1/models | jq .data[1].id
curl -X POST http://localhost:8000/v1/unload_lora_adapter \
-H "Content-Type: application/json" \
-d '{
    "lora_name": "some-lora"
}'
curl -s http://localhost:8000/v1/models | jq .data[1].id

curl -s http://localhost:8000/v1/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "some-lora",
        "prompt": "IBM is a",
        "max_tokens": 17,
        "temperature": 0
    }' | jq
```