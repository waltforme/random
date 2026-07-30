# CUDA checkpoint single-GPU validation

This procedure validates the CUDA checkpoint changes from vLLM PRs #37921
and #37925 after correcting the CUDA Driver API bindings in commit
`2d420a417df625018d3c641df76b43077b1d14a3`. Run every command on the Ubuntu
GPU VM from the repository root.

The corrected extension must use these public CUDA Driver API operations:

- Suspend: `cuCheckpointProcessLock` followed by
  `cuCheckpointProcessCheckpoint`
- Resume: `cuCheckpointProcessRestore` followed by
  `cuCheckpointProcessUnlock`
- State query: `cuCheckpointProcessGetState`

Do not continue if the extension still looks up
`cuCheckpointProcessSuspend` or `cuCheckpointProcessResume`.

## 1. Verify the checkout and host prerequisites

```bash
git status --short --branch
git log --oneline -6
git merge-base --is-ancestor \
  2d420a417df625018d3c641df76b43077b1d14a3 HEAD
echo $?
uname -s
uname -m
nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv
nvcc --version
free -h
```

Requirements:

- Linux on x86-64
- NVIDIA driver 570 or newer
- CUDA toolkit 12.8 or newer
- Enough free host RAM to hold all GPU allocations being checkpointed
- The combined PR branch plus the corrected Driver API bindings

Driver 595.71.05 with a CUDA 12.8 build satisfies the stated version
requirements. The `merge-base` command must print `0`; any other value means
the corrected binding commit is not present in the checkout.

## 2. Build the corrected C++ extension from source

For a new environment:

```bash
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
uv pip install pytest pytest-asyncio tblib
```

For an existing environment, activate it and rebuild after changing the C++
source:

```bash
source .venv/bin/activate
uv pip install pytest pytest-asyncio tblib
uv pip install --reinstall -e .
```

Do not set `VLLM_USE_PRECOMPILED=1`; this test requires the locally modified
C++ extension. If the focused tests report another missing test dependency,
install the complete pinned test set with:

```bash
uv pip install -r requirements/test.txt
```

## 3. Verify the loaded extension and runtime symbols

```bash
.venv/bin/python - <<'PY'
import ctypes
import os

import torch
import vllm.cuda_checkpoint as extension
from vllm.device_allocator.cuda_checkpoint import (
    PROCESS_STATE_RUNNING,
    cuda_checkpoint_available,
)

driver = ctypes.CDLL("libcuda.so.1")
required = (
    "cuCheckpointProcessLock",
    "cuCheckpointProcessCheckpoint",
    "cuCheckpointProcessRestore",
    "cuCheckpointProcessUnlock",
    "cuCheckpointProcessGetState",
)

print("extension:", extension.__file__)
for symbol in required:
    assert hasattr(driver, symbol), f"missing driver symbol: {symbol}"
    print("FOUND", symbol)

print("extension is_available():", extension.is_available())
print("wrapper available:", cuda_checkpoint_available)
assert extension.is_available()
assert cuda_checkpoint_available

torch.cuda.init()
state = extension.get_state(os.getpid())
print("current process state:", state)
assert state == PROCESS_STATE_RUNNING
PY
```

Both availability values must be `True`. Confirm that `extension.__file__`
points into this checkout, not another vLLM installation. The initial process
state must be `0` (`CU_PROCESS_STATE_RUNNING`); this also validates that
`get_state` passes a PID using the corrected signature.

## 4. Run the low-level checkpoint tests

```bash
.venv/bin/python -m pytest \
  tests/basic_correctness/test_cuda_checkpoint.py -v -s
```

Expected result: five tests pass. Skipped tests are not a successful result;
they mean the runtime capability probe returned false.

These tests cover tensor preservation, CUDA graph preservation, repeated-state
errors, and explicit and implicit resume state.

## 5. Start a single-GPU vLLM server

In terminal A:

```bash
CUDA_VISIBLE_DEVICES=0 \
VLLM_SERVER_DEV_MODE=1 \
.venv/bin/vllm serve facebook/opt-125m \
  --host 127.0.0.1 \
  --served-model-name checkpoint-test \
  --tensor-parallel-size 1 \
  --pipeline-parallel-size 1 \
  --dtype float16 \
  --max-model-len 512 \
  --max-num-seqs 4 \
  --gpu-memory-utilization 0.25 \
  --port 8000
```

Replace `facebook/opt-125m` with a local model path if the VM cannot download
from Hugging Face. Do not add `--enforce-eager`, because CUDA graph survival is
part of the validation. No sleep-mode flag is needed.

If 0.25 does not leave enough room for the model and KV cache, increase
`--gpu-memory-utilization` while ensuring the corresponding GPU allocation can
fit in free host RAM during suspension.

The explicit localhost binding keeps the development endpoints off external
interfaces. Use SSH port forwarding if the client is not running on the VM.

## 6. Validate the routes and record baseline inference

In terminal B, wait for the server to become healthy:

```bash
curl --fail --silent --show-error http://localhost:8000/health
curl --fail --silent --show-error http://localhost:8000/is_suspended
```

The state response must be:

```json
{"is_suspended":false}
```

Confirm API validation without changing state:

```bash
curl --silent --show-error --output /dev/null \
  --write-out 'invalid mode: HTTP %{http_code}\n' \
  --request POST 'http://localhost:8000/suspend?mode=invalid'
```

The response code must be 400.

Record deterministic inference before suspension:

```bash
curl --fail --silent --show-error \
  http://localhost:8000/v1/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "checkpoint-test",
    "prompt": "The capital of France is",
    "max_tokens": 8,
    "temperature": 0
  }' > /tmp/cuda-checkpoint-before.json

.venv/bin/python -m json.tool /tmp/cuda-checkpoint-before.json
```

## 7. Suspend and inspect released GPU resources

Optionally monitor GPU usage in terminal C:

```bash
watch -n 0.5 nvidia-smi
```

With no inference request active, suspend from terminal B:

```bash
curl --fail --silent --show-error --output /dev/null \
  --write-out 'suspend: HTTP %{http_code}, %{time_total}s\n' \
  --request POST 'http://localhost:8000/suspend?mode=abort'

curl --fail --silent --show-error http://localhost:8000/is_suspended
```

Expected results:

- `/suspend` returns HTTP 200.
- `/is_suspended` returns `{"is_suspended":true}`.
- The worker's GPU memory usage disappears or drops substantially.
- Server logs report successful lock/checkpoint and suspend timing.

Do not send inference requests while the scheduler is suspended.

## 8. Resume and compare inference results

```bash
curl --fail --silent --show-error --output /dev/null \
  --write-out 'resume: HTTP %{http_code}, %{time_total}s\n' \
  --request POST http://localhost:8000/resume

curl --fail --silent --show-error http://localhost:8000/is_suspended
```

The state must return to `{"is_suspended":false}`, and GPU memory should return.

Run the same deterministic request:

```bash
curl --fail --silent --show-error \
  http://localhost:8000/v1/completions \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "checkpoint-test",
    "prompt": "The capital of France is",
    "max_tokens": 8,
    "temperature": 0
  }' > /tmp/cuda-checkpoint-after.json

.venv/bin/python - <<'PY'
import json

with open("/tmp/cuda-checkpoint-before.json") as file:
    before = json.load(file)["choices"][0]["text"]
with open("/tmp/cuda-checkpoint-after.json") as file:
    after = json.load(file)["choices"][0]["text"]

print("before:", repr(before))
print("after: ", repr(after))
assert before == after, "deterministic completion changed after restore"
print("PASS: inference output was preserved")
PY
```

## 9. Exercise repeated cycles and shut down cleanly

Run several idle suspend/resume cycles:

```bash
for cycle in 1 2 3; do
  echo "cycle $cycle: suspend"
  curl --fail --silent --show-error --request POST \
    'http://localhost:8000/suspend?mode=abort'
  curl --fail --silent --show-error http://localhost:8000/is_suspended

  echo "cycle $cycle: resume"
  curl --fail --silent --show-error --request POST \
    http://localhost:8000/resume
  curl --fail --silent --show-error http://localhost:8000/is_suspended
done
```

Run one final inference request after the loop. Before stopping the server,
confirm that it is resumed:

```bash
curl --fail --silent --show-error http://localhost:8000/is_suspended
```

Only stop terminal A after the response is `{"is_suspended":false}`.

## Success criteria

The validation succeeds only if all of the following hold:

- The official CUDA checkpoint symbols are present.
- Both Python availability checks return true.
- All five low-level tests pass without skips.
- The live server transitions from running to suspended and back.
- GPU resources are released during suspension and reacquired on resume.
- Deterministic inference output is unchanged after restore.
- Repeated suspend/resume cycles complete without crashes or CUDA errors.

## Common failures

- **`is_available()` is false:** verify the rebuilt extension is loaded and
  that its capability probe uses Lock/Checkpoint/Restore/Unlock, not the
  nonexistent Suspend/Resume symbols.
- **Tests are skipped:** treat this as a capability-probe failure, not success.
- **HTTP 404:** restart the server with `VLLM_SERVER_DEV_MODE=1` set before
  process startup.
- **CUDA out-of-memory or host out-of-memory:** lower
  `--gpu-memory-utilization`, use a smaller model, or add host RAM.
- **`destroy` or `reinit` errors from pynccl:** confirm TP=1, PP=1, and a total
  parallel world size of one.
- **Server fails only during suspend/resume:** preserve the full worker logs and
  the numeric CUDA error code; the PRs are in flight and do not yet have full
  integration coverage.
- **Checkpoint fails after locking:** stop the isolated test process or server
  rather than continuing to issue CUDA work; a failed transition can leave the
  CUDA process in `LOCKED` or `FAILED` state.
