# vLLM CUDA Checkpoint/Restore Testing

Test run of two in-flight vLLM PRs, [#37921](https://github.com/vllm-project/vllm/pull/37921) and [#37925](https://github.com/vllm-project/vllm/pull/37925).

These two PRs implement CUDA-based GPU checkpoint/restore, targeting the "Tier 1: In-Process CUDA Suspend/Resume" approach proposed in [RFC #34303](https://github.com/vllm-project/vllm/issues/34303).

## Result
Successful test runs, but only after non-trivial changes to how the NVIDIA driver APIs are used.

## Steps
First, the two PRs were merged together into a local branch, so that the core functionality built by #37921 could be driven through the API endpoints exposed by #37925.

Next, it became clear that changes to the NVIDIA driver API usage were necessary. Specifically:
1. The symbols `cuCheckpointProcessSuspend` and `cuCheckpointProcessResume` called by `csrc/cuda_checkpoint.cpp` don't appear to exist in the CUDA Checkpointing driver API.
2. `csrc/cuda_checkpoint.cpp` diverged from the RFC, which proposed exposing `lock()`, `checkpoint()`, `restore()`, `unlock()`, `get_state()`, and `is_supported()` (a runtime feature gate that probes for driver ≥ 570).

My changes switched to the API exposed by the CUDA Checkpointing driver and restored the RFC's five-primitive surface.

Finally, with these changes in place, I was able to successfully exercise CUDA-based GPU checkpoint/restore via the `/suspend`, `/resume`, and `/is_suspended` API endpoints.

## Details About the Changed Code
The successfully tested code now lives in branch [`try-cuda-checkpoint`](https://github.com/waltforme/vllm/tree/try-cuda-checkpoint) of my vLLM fork, which is [6 commits ahead of](https://github.com/vllm-project/vllm/compare/main...waltforme:vllm:try-cuda-checkpoint) `main`:
- The first 4 commits come from PRs #37921 and #37925.
- The fifth commit merges the two PRs.
- **The sixth commit contains the changes that switch to the CUDA Checkpointing driver's exposed API and restore the RFC's five-primitive surface.**

I'd be glad to work with @elizabetht to fold these changes into #37921/#37925, if she's open to it.

## Details About the Documentation
- [procedure.md](./procedure.md) shares a reproducible procedure for anyone to wants to tryout the test run.
- [terminal_A.txt](./terminal_A.txt) captures the unit test results and vLLM log of the test run.
- [terminal_B.txt](./terminal_B.txt) captures the commands issued against the vLLM instance during the test run.

## Motivation
The [FMA](https://github.com/llm-d-incubation/llm-d-fast-model-actuation) team is looking to integrate this GPU checkpoint/restore capability. Ideally it would merge into vLLM through these two PRs, enabling FMA's seamless integration.
