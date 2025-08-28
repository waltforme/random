Sometimes the vLLM container is able to see all GPUs of a node.
But the reason is not clear yet.
This experiment finds the reason and present some extra discussions.

I short, the reason is that the vLLM container image has the envar `NVIDIA_VISIBLE_DEVICES=all` baked in.


## When does the vLLM container see all GPUs?
As documented in [a previous experiment](./grpc_call_from_kubelet_to_container-runtime.md), 
the vLLM container is able to see all GPUs of a node when two conditions are both met.
1. Remove or set zero value to `nvidia.com/gpu` in `Container.Resources` of the PodSpec;
2. Unset the `NVIDIA_VISIBLE_DEVICES` envar in `Container.Env` of the PodSpec.

To confirm that, check the `nvidia-container-cli`'s `--device=all` flag.
```txt
nvidia-containe  29559  29557    0 /usr/local/nvidia/toolkit/nvidia-container-cli --root=/ --load-kmods configure --cuda-compat-mode=ldconfig --ldconfig=@/sbin/ldconfig.real --device=all --compute --utility --require=cuda>=12.4 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<47 --pid=29550 /var/lib/docker/overlay2/09ff1b18f06aa29c4cb1c65ac45cecfb2b3d63643f2bac37bbc631436eed2a81/merged 
```

**It turns out the `--device=all` flag comes from the `NVIDIA_VISIBLE_DEVICES=all` envar that baked into the vLLM container image.**
Let me verify that as follows.


## Change the vLLM container image by setting `NVIDIA_VISIBLE_DEVICES` to emtpy
Confirm the value of `NVIDIA_VISIBLE_DEVICES` envar is `all` in the vLLM container image.
```console
$ docker inspect vllm/vllm-openai:v0.8.5 | jq '.[0].Config.Env'
[
  "PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin",
  "NVARCH=x86_64",
  "NVIDIA_REQUIRE_CUDA=cuda>=12.4 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<471 brand=nvidiartx,driver>=470,driver<471 brand=geforce,driver>=470,driver<471 brand=geforcertx,driver>=470,driver<471 brand=quadro,driver>=470,driver<471 brand=quadrortx,driver>=470,driver<471 brand=titan,driver>=470,driver<471 brand=titanrtx,driver>=470,driver<471 brand=tesla,driver>=525,driver<526 brand=unknown,driver>=525,driver<526 brand=nvidia,driver>=525,driver<526 brand=nvidiartx,driver>=525,driver<526 brand=geforce,driver>=525,driver<526 brand=geforcertx,driver>=525,driver<526 brand=quadro,driver>=525,driver<526 brand=quadrortx,driver>=525,driver<526 brand=titan,driver>=525,driver<526 brand=titanrtx,driver>=525,driver<526 brand=tesla,driver>=535,driver<536 brand=unknown,driver>=535,driver<536 brand=nvidia,driver>=535,driver<536 brand=nvidiartx,driver>=535,driver<536 brand=geforce,driver>=535,driver<536 brand=geforcertx,driver>=535,driver<536 brand=quadro,driver>=535,driver<536 brand=quadrortx,driver>=535,driver<536 brand=titan,driver>=535,driver<536 brand=titanrtx,driver>=535,driver<536",
  "NV_CUDA_CUDART_VERSION=12.4.99-1",
  "NV_CUDA_COMPAT_PACKAGE=cuda-compat-12-4",
  "CUDA_VERSION=12.4.0",
  "LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64",
  "NVIDIA_VISIBLE_DEVICES=all",
  "NVIDIA_DRIVER_CAPABILITIES=compute,utility",
  "NV_CUDA_LIB_VERSION=12.4.0-1",
  "NV_NVTX_VERSION=12.4.99-1",
  "NV_LIBNPP_VERSION=12.2.5.2-1",
  "NV_LIBNPP_PACKAGE=libnpp-12-4=12.2.5.2-1",
  "NV_LIBCUSPARSE_VERSION=12.3.0.142-1",
  "NV_LIBCUBLAS_PACKAGE_NAME=libcublas-12-4",
  "NV_LIBCUBLAS_VERSION=12.4.2.65-1",
  "NV_LIBCUBLAS_PACKAGE=libcublas-12-4=12.4.2.65-1",
  "NV_LIBNCCL_PACKAGE_NAME=libnccl2",
  "NV_LIBNCCL_PACKAGE_VERSION=2.20.5-1",
  "NCCL_VERSION=2.20.5-1",
  "NV_LIBNCCL_PACKAGE=libnccl2=2.20.5-1+cuda12.4",
  "NVIDIA_PRODUCT_NAME=CUDA",
  "NV_CUDA_CUDART_DEV_VERSION=12.4.99-1",
  "NV_NVML_DEV_VERSION=12.4.99-1",
  "NV_LIBCUSPARSE_DEV_VERSION=12.3.0.142-1",
  "NV_LIBNPP_DEV_VERSION=12.2.5.2-1",
  "NV_LIBNPP_DEV_PACKAGE=libnpp-dev-12-4=12.2.5.2-1",
  "NV_LIBCUBLAS_DEV_VERSION=12.4.2.65-1",
  "NV_LIBCUBLAS_DEV_PACKAGE_NAME=libcublas-dev-12-4",
  "NV_LIBCUBLAS_DEV_PACKAGE=libcublas-dev-12-4=12.4.2.65-1",
  "NV_CUDA_NSIGHT_COMPUTE_VERSION=12.4.0-1",
  "NV_CUDA_NSIGHT_COMPUTE_DEV_PACKAGE=cuda-nsight-compute-12-4=12.4.0-1",
  "NV_NVPROF_VERSION=12.4.99-1",
  "NV_NVPROF_DEV_PACKAGE=cuda-nvprof-12-4=12.4.99-1",
  "NV_LIBNCCL_DEV_PACKAGE_NAME=libnccl-dev",
  "NV_LIBNCCL_DEV_PACKAGE_VERSION=2.20.5-1",
  "NV_LIBNCCL_DEV_PACKAGE=libnccl-dev=2.20.5-1+cuda12.4",
  "LIBRARY_PATH=/usr/local/cuda/lib64/stubs",
  "DEBIAN_FRONTEND=noninteractive",
  "UV_HTTP_TIMEOUT=500",
  "VLLM_USAGE_SOURCE=production-docker-image"
]
```

Make a change to the container image.
```Dockerfile
FROM vllm/vllm-openai:v0.8.5

ENV NVIDIA_VISIBLE_DEVICES=
```

Check the value in the modified image.
```console
$ docker inspect vllm-empty-nvd:latest | jq '.[0].Config.Env' | grep VISIBLE
  "NVIDIA_VISIBLE_DEVICES=",
```

Now keep the two conditions in [When does the vLLM container see all GPUs?](#when-does-the-vllm-container-see-all-gpus) met, but try to use this modified image.
Here is my observations.
- `docker inspect` shows that `NVIDIA_VISIBLE_DEVICES=` for the vLLM container.
- The vLLM pod keeps crashing and says `[__init__.py:243] No platform detected, vLLM is running on UnspecifiedPlatform`.
- `nvidia-smi` is not available in the container. I got `OCI runtime exec failed: exec failed: unable to start container process: exec: "nvidia-smi": executable file not found in $PATH: unknown`.
- I didn't see `nvidia-container-cli` called by `nvidia-container-runtime-hook`.

All these observations suggest that the empty value of `NVIDIA_VISIBLE_DEVICES` inside the vLLM container image takes effect.


## Change the vLLM container image by setting `NVIDIA_VISIBLE_DEVICES` for a specific GPU
I also tried another change to the vLLM container image,
by saying `ENV NVIDIA_VISIBLE_DEVICES=GPU-c1503c34-3335-4ddd-2c08-646b0a6c0041`, where the value is the UUID of one GPU on the node.
```Dockerfile
FROM vllm/vllm-openai:v0.8.5

ENV NVIDIA_VISIBLE_DEVICES=GPU-c1503c34-3335-4ddd-2c08-646b0a6c0041
```

Here are my observations.
- `docker inspect` shows that `NVIDIA_VISIBLE_DEVICES=GPU-c1503c34-3335-4ddd-2c08-646b0a6c0041` for the vLLM container.
- The vLLM pod runs successfully using the specified GPU.
- I see `nvidia-container-cli` called with `--device=GPU-c1503c34-3335-4ddd-2c08-646b0a6c0041`, instead of the previously seen `--device=all`.
    ```
    nvidia-containe  15095  15093    0 /usr/local/nvidia/toolkit/nvidia-container-cli --root=/ --load-kmods configure --cuda-compat-mode=ldconfig --ldconfig=@/sbin/ldconfig.real --device=GPU-c1503c34-3335-4ddd-2c08-646b0a6c0041 --compute --utility --require=cuda>=12.4 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<47 --pid=15086 /var/lib/docker/overlay2/638d1d4fe4f3d5aca6f723b74facbd09bbbc6a4ed7b6399053bbc8a2db3ecad5/merged 
    ```

All these observations suggest that the particular value of `NVIDIA_VISIBLE_DEVICES` inside the vLLM container image takes effect.

**If empty value and particular GPU UUID both take effect, I can safely say the original `all` value is also effective.**

Is there a way to remove (i.e. unset) an envar from a container image?
I didn't find such a way. So I tried an empty value and a particular value, but couldn't try a modified image with the envar completely erased.

## Some more trials and discussions on the order of precedence and defaulting
### Order of precedence
In this part, I want to confirm the order of precedence between two `NVIDIA_VISIBLE_DEVICES` envars.
- The 1st one is [the last instance](./independent_kubelet_and_nvidia-container-cli.md) of `NVIDIA_VISIBLE_DEVICES` in `ContainerConfig` that is used by the gPRC call from kubelet to container runtime;
- The 2nd one is in the vLLM container image.

I still kept condition 1 in [When does the vLLM container see all GPUs?](#when-does-the-vllm-container-see-all-gpus) met.
But set `NVIDIA_VISIBLE_DEVICES=void` in `Container.Env` of the PodSpec.
This way, the 1st one takes value `void`.

I used the unmodified image so that it has `NVIDIA_VISIBLE_DEVICES=all` baked in.
This way, the 2nd one takes value `all`.

Here is what I observed.
- `docker inspect` shows that `NVIDIA_VISIBLE_DEVICES=void` for the vLLM container.
- The vLLM pod keeps crashing and logs `[__init__.py:243] No platform detected, vLLM is running on UnspecifiedPlatform`.
- `nvidia-smi` is not available in the container. I got `OCI runtime exec failed: exec failed: unable to start container process: exec: "nvidia-smi": executable file not found in $PATH: unknown`.
- I didn't see `nvidia-container-cli` called by `nvidia-container-runtime-hook`.

All these observations suggest that `NVIDIA_VISIBLE_DEVICES` in `ContainerConfig` takes precedence over the one in container image.

### Defaulting (not for vLLM)
What if `NVIDIA_VISIBLE_DEVICES` is set nowhere?

I've heard of some defaulting logic of nvidia container runtime.
I was able to find that the nvidia container toolkit has [this logic](https://github.com/NVIDIA/nvidia-container-toolkit/blob/eb725b35c49e59370aeabfe80759d5d810b6851c/internal/config/image/cuda_image.go#L167-L175) for a 'legacy image'.
```go
	// Environment variable unset with legacy image: default to "all".
	if !isSet && len(devices) == 0 && i.IsLegacy() {
		devices = []string{"all"}
	}

	// Environment variable unset or empty or "void": return nil
	if len(devices) == 0 || requested["void"] {
		devices = []string{"void"}
	}
```

I'm not sure what is considered as a 'legacy image'.
But since the vLLM container image *has* `NVIDIA_VISIBLE_DEVICES=all`,
this defaulting logic is *not* the reason why all GPUs are visible inside the vLLM container.

## Conclusion
If `NVIDIA_VISIBLE_DEVICES` is not present when kubelet calls container runtime,
then `NVIDIA_VISIBLE_DEVICES=all` inside the vLLM container takes the precedence,
thus makes all GPUs visible inside the vLLM container.
