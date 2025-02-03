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

```shell
kind create cluster --config=./vllm-lora/kind/cluster_lora.yaml

pushd ./vllm-lora/preparer
docker build -t myrepo/prepare-adapters:latest .
kind load --name lora docker-image myrepo/prepare-adapters:latest
docker exec lora-control-plane crictl images
popd

kubectl apply -f ./vllm-lora/pvc_shared-adapters.yaml
kubectl apply -f ./vllm-lora/job_prepare-adapters.yaml
kubectl logs job/prepare-adapters # "All adapters downloaded successfully."

# Build in the root dir of your clone of https://github.com/vllm-project/vllm.git.
# This experiment uses commit dd6a3a02cb3bf2a7bc6cb84c85dcd57c6eaf2bf9.
docker build -f Dockerfile.cpu -t vllm-cpu-env --shm-size=4g .
kind load --name lora docker-image vllm-cpu-env:latest
docker exec lora-control-plane crictl images

kubectl apply -f ./vllm-lora/deployment_qwen2.yaml
kubectl wait --for=condition=Available deployment/qwen2 --timeout=300s
kubectl apply -f ./vllm-lora/service_qwen2.yaml
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

# sharing adapters
kubectl apply -f ./vllm-lora/deployment_qwen2-copy.yaml
kubectl wait --for=condition=Available deployment/qwen2-copy --timeout=300s
kubectl apply -f ./vllm-lora/service_qwen2-copy.yaml
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

```shell
vllm serve Qwen/Qwen2-0.5B-Instruct \
    --enable-lora \
    --lora-modules some-lora=$HOME/.cache/huggingface/hub/models--sikoraaxd--Qwen2-0.5B-Instruct-ru-lora/snapshots/f1fa56303ae329d2c19f61e2fd51a82c48e32003/
# alternatively
python3 -m vllm.entrypoints.openai.api_server --model Qwen/Qwen2-0.5B-Instruct \
    --enable-lora \
    --lora-modules some-lora=$HOME/.cache/huggingface/hub/models--sikoraaxd--Qwen2-0.5B-Instruct-ru-lora/snapshots/f1fa56303ae329d2c19f61e2fd51a82c48e32003/

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