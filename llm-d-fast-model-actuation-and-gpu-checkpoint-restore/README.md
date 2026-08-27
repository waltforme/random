## FMA's Adoption of vLLM-Based GPU Checkpoint/Restore
This experiment explores how [FMA](https://github.com/llm-d-incubation/llm-d-fast-model-actuation) can adopt GPU Checkpoint/Restore technology to provide another path for fast model actuation.

This experiment uses work from the in-flight PRs https://github.com/vllm-project/vllm/pull/37921 and https://github.com/vllm-project/vllm/pull/37925 which aim to integrate GPU Checkpoint/Restore into vLLM. For more details, see https://github.com/waltforme/random/tree/main/vllm-cuda-checkpoint-testing.


### Main results
Scale the FMA server request down to zero replicas: The FMA 'dual pods' unbind, and the launcher becomes 'suspended' (i.e., CUDA-checkpointed).
```console
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" scale rs/gpucr-request --replicas=0
replicaset.apps/gpucr-request scaled
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" get pods -w   -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,DUAL:.metadata.labels.dual-pods\.llm-d\.ai/dual,SUSPENDED:.metadata.labels.dual-pods\.llm-d\.ai/sleeping'
NAME                                        STATUS    DUAL     SUSPENDED
fma-dual-pods-controller-6cf57f86b4-x8kq5   Running   <none>   <none>
launcher-gpucr-lc-rhpkx                     Running   <none>   true
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" exec "${LAUNCHER_POD}" -c inference-server -- \ \
  curl -s localhost:${VLLM_PORT}/is_suspended
{"is_suspended":true}
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ nvidia-smi
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.71.05              Driver Version: 595.71.05      CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA L4                      Off |   00000000:35:00.0 Off |                    0 |
| N/A   43C    P8             16W /   72W |       0MiB /  23034MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|  No running processes found                                                             |
+-----------------------------------------------------------------------------------------+
```

Scale the FMA server request back up to one replica: The FMA 'dual pods' bind, and the launcher resumes serving (within a few seconds).
```console
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" scale rs/gpucr-request --replicas=1
kubectl -n "${NS}" wait --for=condition=Ready pod -l app=gpucr-example --timeout=600s
replicaset.apps/gpucr-request scaled
pod/gpucr-request-b8rvw condition met
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" get pods -w   -o custom-columns='NAME:.metadata.name,STATUS:.status.phase,DUAL:.metadata.labels.dual-pods\.llm-d\.ai/dual,SUSPENDED:.metadata.labels.dual-pods\.llm-d\.ai/sleeping'
NAME                                        STATUS    DUAL                      SUSPENDED
fma-dual-pods-controller-6cf57f86b4-x8kq5   Running   <none>                    <none>
gpucr-request-b8rvw                         Running   launcher-gpucr-lc-rhpkx   <none>
launcher-gpucr-lc-rhpkx                     Running   gpucr-request-b8rvw       false
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ kubectl -n "${NS}" exec "${LAUNCHER_POD}" -c inference-server -- \
  curl -s localhost:${VLLM_PORT}/is_suspended
{"is_suspended":false}
(vllm) ubuntu@ip-172-31-58-228:~/llm-d-fast-model-actuation$ nvidia-smi
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.71.05              Driver Version: 595.71.05      CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA L4                      Off |   00000000:35:00.0 Off |                    0 |
| N/A   50C    P0             35W /   72W |   19874MiB /  23034MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+

+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A           20615      C   VLLM::EngineCore                      19866MiB |
+-----------------------------------------------------------------------------------------+
```


### Details
The full terminal session for the experiment is recorded in [terminal_transcript.txt](./terminal_transcript.txt).

This experiment was conducted using https://github.com/waltforme/llm-d-fast-model-actuation/tree/adopt-vllm-gpucr,
which is an experimental branch of my FMA fork.
This branch:
- Uses a customized launcher image that is based on my customized vLLM. For details about the customized vLLM, see https://github.com/waltforme/random/tree/main/vllm-cuda-checkpoint-testing;
- Makes surgical changes to the dual-pods controller to leverage the customized vLLM's CUDA checkpointing instead of the ordinary vLLM's sleep mode;
- Provides [reproducible steps](https://github.com/waltforme/llm-d-fast-model-actuation/blob/adopt-vllm-gpucr/docs/vllm-gpu-checkpoint-restore-demo.md) for anyone who wants to try this experiment.
