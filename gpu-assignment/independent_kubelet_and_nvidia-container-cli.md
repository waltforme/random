In the [previous experiment](./grpc_call_from_kubelet_to_container-runtime.md), I saw two instances of the `NVIDIA_VISIBLE_DEVICES` envar in `ContainerConfig` that is passed from the kubelet to the container runtime.

Natually, a question is: Which instance is respected? This experiment answers the question.
The short answer is: Whichever appears lastly in the envar list is respected by nvidia container runtime, specifically `nvidia-container-cli`, the one appears firstly is ignored by `nvidia-container-cli`.


## The order of the two instances matters
I wrote a helper function to swap the two instances of the envar.
```go
func swapTheTwoEnvarsInContainerConfig(cfg *runtimeapi.ContainerConfig) {
	// there are two instances of NVIDIA_VISIBLE_DEVICES envars intead of one, because
	// the kubelet injected the first one when handling Container.Resources
	// and a human wrote the second one in Container.Env
	indice := []int{}
	for idx, env := range cfg.Envs {
		if env.Key == "NVIDIA_VISIBLE_DEVICES" {
			klog.Info("MyDebug(envar in ContainerConfig): ", env.Key, env.Value)
			indice = append(indice, idx)
		}
	}
	if len(indice) == 2 {
		klog.Info("MyDebug: switch two envars")
		first, firstE := indice[0], cfg.Envs[indice[0]]
		second, secondE := indice[1], cfg.Envs[indice[1]]
		tmpE := runtimeapi.KeyValue{Key: firstE.Key, Value: firstE.Value}
		cfg.Envs[first] = secondE
		cfg.Envs[second] = &tmpE
	} else {
		klog.Infof("MyDebug: there are %d NVIDIA_VISIBLE_DEVICES env var", len(indice))
	}
	for _, env := range cfg.Envs {
		if env.Key == "NVIDIA_VISIBLE_DEVICES" {
			klog.Info("MyDebug(envar in ContainerConfig): ", env.Key, env.Value)
		}
	}
}
```

Then I checked which instance is used by `nvidia-container-cli`.
It turns out that only the latter is picked up.

When the latter is human-specified:
```txt
nvidia-containe  81337  81335    0 /usr/local/nvidia/toolkit/nvidia-container-cli --root=/ --load-kmods configure --cuda-compat-mode=ldconfig --ldconfig=@/sbin/ldconfig.real --device=3 --compute --utility --require=cuda>=12.4 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<47 --pid=81328 /var/lib/docker/overlay2/3e1189f69adddc002c9bf7804eaba6e8e335edcc11bb03b3bc58c0038c5f36bb/merged
```
When the latter is kubelet-injected (swapped):
```txt
nvidia-containe  74605  74604    0 /usr/local/nvidia/toolkit/nvidia-container-cli --root=/ --load-kmods configure --cuda-compat-mode=ldconfig --ldconfig=@/sbin/ldconfig.real --device=GPU-376c6d02-728d-90f0-c978-dc0e8392cdce --compute --utility --require=cuda>=12.4 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<47 --pid=74596 /var/lib/docker/overlay2/066aecd72d6d47be3d077efb16f3f7351567aa00a13678e1594539bc9eb5c8a3/merged
```
So the order of the two instances matters.

I also noticed that the kubelet-injected instance is always the 1st one in the list of envars, and the human-specified instance is somewhere else in the list.
For example,
```go
&KeyValue{Key: NVIDIA_VISIBLE_DEVICES, Value: GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783},
&KeyValue{Key: NVIDIA_VISIBLE_DEVICES, Value: 3},
&KeyValue{Key: VLLM_SERVER_DEV_MODE, Value: 1},
&KeyValue{Key: HF_HOME, Value: /tmp},
&KeyValue{Key: POD_IP, Value: 10.0.2.140},
&KeyValue{Key: LMCACHE_LOG_LEVEL, Value: DEBUG},
&KeyValue{Key: VLLM_USE_V1, Value: 1},
&KeyValue{Key: EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_9999_TCP_ADDR, Value: 10.107.5.252},
&KeyValue{Key: KUBERNETES_SERVICE_PORT, Value: 443},
&KeyValue{Key: KUBERNETES_PORT, Value: tcp://10.96.0.1:443},
&KeyValue{Key: KUBERNETES_PORT_443_TCP_PORT, Value: 443},
```

This explains why the vLLM pod *always* see the human specified GPU, but only *usualy* (when the corresponding GPUs of the two envar instances differ) see the kubelet-injected GPU.


## The kubelet injected '/dev/nvidiaX' is effective
Note that the kubelet not only injects an instance of the `NVIDIA_VISIBLE_DEVICES` envar, but also injects a set of devices into `ContainerConfig.Devices`.
```go
Devices:[]*Device{
    &Device{ContainerPath:/dev/nvidiactl,HostPath:/dev/nvidiactl,Permissions:rw,},
    &Device{ContainerPath:/dev/nvidia-uvm,HostPath:/dev/nvidia-uvm,Permissions:rw,},
    &Device{ContainerPath:/dev/nvidia-uvm-tools,HostPath:/dev/nvidia-uvm-tools,Permissions:rw,},
    &Device{ContainerPath:/dev/nvidia-modeset,HostPath:/dev/nvidia-modeset,Permissions:rw,},
    &Device{ContainerPath:/dev/nvidia1,HostPath:/dev/nvidia1,Permissions:rw,},
}
```

I suspect this set of devices are still effective even when the kubelet-injected instance of envar is ignored by `nvidia-container-cli`.

To confirm, I didn't swap the two envars to keep the kubelet-injected envar ignored by `nvidia-container-cli`.
Then I deleted the GPU that injected into ContainerConfig by the kubelet.
```go
func deleteTheInjectedDevFromContainerConfig(cfg *runtimeapi.ContainerConfig) {
	regex := regexp.MustCompile(`^/dev/nvidia[0-9]$`)
	for i, dev := range cfg.Devices {
		if regex.MatchString(dev.ContainerPath) {
			klog.InfoS("MyDebug: Removing the injected device from ContainerConfig", "device", dev.ContainerPath)
			len := len(cfg.Devices)
			cfg.Devices[i] = cfg.Devices[len-1]
			cfg.Devices = cfg.Devices[:len-1]
			break
		}
	}
}
```

As a result, the corresponding GPU is not visible anymore in the vLLM container.


## Both the kubelet and the nvidia-container-cli can independently assign GPUs
Note that the kubelet injects a set of devices into `ContainerConfig.Devices`.
The set includes the GPU, '/dev/nvidiaX', as well as some other 'supportive' devices.
```txt
root@sjqoxho6on-granite-3-2-2b-instruct-vllm-stack:/vllm-workspace# ls -l /dev/nvidia*
crw-rw-rw- 1 root root 195, 254 Aug 23 18:59 /dev/nvidia-modeset
crw-rw-rw- 1 root root 235,   0 Aug 23 18:32 /dev/nvidia-uvm
crw-rw-rw- 1 root root 235,   1 Aug 23 18:32 /dev/nvidia-uvm-tools
crw-rw-rw- 1 root root 195,   1 Aug 23 18:59 /dev/nvidia1
crw-rw-rw- 1 root root 195, 255 Aug 23 18:30 /dev/nvidiactl
```

What if I also delete the kubelet-injected 'supportive' devices?

To investigate, I didn't swap the two envars to keep kubelet-injected envar ignored.
Then I deleted all the devices, including the GPU and the 'supportive' devices, that injected into ContainerConfig by the kubelet.
```go
func deleteAllInjectedDevsFromContainerConfig(cfg *runtimeapi.ContainerConfig) {
	regex := regexp.MustCompile(`^/dev/nvidia.*`)
	cleanedDevs := []*runtimeapi.Device{}
	for _, dev := range cfg.Devices {
		if regex.MatchString(dev.ContainerPath) {
			klog.InfoS("MyDebug: Ignoring one injected device from ContainerConfig", "device", dev.ContainerPath)
			continue
		}
		cleanedDevs = append(cleanedDevs, dev)
	}
	cfg.Devices = cleanedDevs
}
```

Turns out that `nvidia-container-cli` can by its own setup 'supportive' devices such as '/dev/nvidiactl'.
```txt
root@ckjdqefd30-granite-3-2-2b-instruct-vllm-stack:/vllm-workspace# ls -l /dev/nvidia*
crw-rw-rw- 1 root root 235,   0 Aug 14 18:47 /dev/nvidia-uvm
crw-rw-rw- 1 root root 235,   1 Aug 14 18:47 /dev/nvidia-uvm-tools
crw-rw-rw- 1 root root 195,   3 Aug 14 18:44 /dev/nvidia3
crw-rw-rw- 1 root root 195, 255 Aug 14 18:44 /dev/nvidiactl
```
There is slight difference though, which is `nvidia-container-cli` didn't inject `/dev/nvidia-modeset`.

So, kubelet-injected 'supportive' devices can be safely removed from the ContainerConfig before kubelet issuing CreateContainer call through CRI.
As long as a valid `NVIDIA_VISIBLE_DEVICES`, which is the human-specified one here, exists in the ContainerConfig.
`nvidia-container-cli` will consume the valid `NVIDIA_VISIBLE_DEVICES` and setup the GPU and the 'supportive' devices.


## Conclusions
- The order of the two instances of `NVIDIA_VISIBLE_DEVICES` in `ContainerConfig.Envs` matters. Only the latter is picked up by `nvidia-container-cli`.
- Both the kubelet and the `nvidia-container-cli` can independently assign GPUs, including the 'supportive' devices.
