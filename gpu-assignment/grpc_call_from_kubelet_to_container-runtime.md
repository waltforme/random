To better understand the GPU assignment procedure, I checked the gRPC call from the kubelet to the container runtime. 

I added additional logging to the kubelet source to show the `ContainerConfig` that is consumed by the `CreateContainer` gRPC call, which is [part of the interface](https://github.com/kubernetes/kubernetes/blob/69e56f33ca11dd60faf1bf8b3893d3102b9270a1/staging/src/k8s.io/cri-api/pkg/apis/services.go#L36) between the kubelet and the container runtime.

## Two instances of the `NVIDIA_VISIBLE_DEVICES` envar

There are two instances of the `NVIDIA_VISIBLE_DEVICES` envar in the `ContainerConfig`, where
1. The 1st instance corresponds to the GPU(s) injected by the kubelet, based on the device plugin's preferred allocation. This one uses UUID(s) by default;
2. The 2nd instance corresponds to the GPU(s) specified by me in `PodSpec.Container.Env`.

Below is what I saw from the additional logging.
```text
Aug 18 20:24:55 ip-172-31-51-22 kubelet[12071]: I0818 20:24:55.662663   12071 manager.go:1027] "MyDebug: Issuing a GetPreferredAllocation call for container" containerName="vllm" podUID="1dbf314f-cf74-4181-8e4d-2aa0599d79c3"
Aug 18 20:25:05 ip-172-31-51-22 kubelet[12071]: I0818 20:25:05.238166   12071 manager.go:1029] MyDebug(show PreferredAllocationResponse): &PreferredAllocationResponse{ContainerResponses:[]*ContainerPreferredAllocationResponse{&ContainerPreferredAllocationResponse{DeviceIDs:[GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783],},},}
Aug 18 20:25:05 ip-172-31-51-22 kubelet[12071]: I0818 20:25:05.238244   12071 manager.go:853] MyDebug(show allocDevices): map[GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783:{}]
Aug 18 20:25:05 ip-172-31-51-22 kubelet[12071]: I0818 20:25:05.238281   12071 manager.go:889] "MyDebug: Making allocation request for device plugin" devices=["GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783"] resourceName="nvidia.com/gpu"
Aug 18 20:25:05 ip-172-31-51-22 kubelet[12071]: I0818 20:25:05.239015   12071 manager.go:891] MyDebug(show AllocateResponse): &AllocateResponse{ContainerResponses:[]*ContainerAllocateResponse{&ContainerAllocateResponse{Envs:map[string]string{NVIDIA_VISIBLE_DEVICES: GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783,},Mounts:[]*Mount{},Devices:[]*DeviceSpec{&DeviceSpec{ContainerPath:/dev/nvidiactl,HostPath:/dev/nvidiactl,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-uvm,HostPath:/dev/nvidia-uvm,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-uvm-tools,HostPath:/dev/nvidia-uvm-tools,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-modeset,HostPath:/dev/nvidia-modeset,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia0,HostPath:/dev/nvidia0,Permissions:rw,},},Annotations:map[string]string{},CDIDevices:[]*CDIDevice{},},},}
Aug 18 20:25:06 ip-172-31-51-22 kubelet[12071]: I0818 20:25:06.599190   12071 kuberuntime_container.go:266] MyDebug(show containerConfig): &ContainerConfig{Metadata:&ContainerMetadata{Name:vllm,Attempt:0,},Image:&ImageSpec{Image:vllm/vllm-openai@sha256:6cf9808ca8810fc6c3fd0451c2e7784fb224590d81f7db338e7eaf3c02a33d33,Annotations:map[string]string{},UserSpecifiedImage:vllm/vllm-openai:v0.8.5,RuntimeHandler:,},Command:[vllm serve ibm-granite/granite-3.2-2b-instruct --host 0.0.0.0 --port 8000 --no-enable-prefix-caching --enable-sleep-mode],Args:[],WorkingDir:,Envs:[]*KeyValue{&KeyValue{Key:NVIDIA_VISIBLE_DEVICES,Value:GPU-8519f552-3983-e6d6-b2f0-f4a9fccad783,},&KeyValue{Key:NVIDIA_VISIBLE_DEVICES,Value:3,},&KeyValue{Key:VLLM_SERVER_DEV_MODE,Value:1,},&KeyValue{Key:HF_HOME,Value:/tmp,},&KeyValue{Key:POD_IP,Value:10.0.2.140,},&KeyValue{Key:LMCACHE_LOG_LEVEL,Value:DEBUG,},&KeyValue{Key:VLLM_USE_V1,Value:1,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_9999_TCP_ADDR,Value:10.107.5.252,},&KeyValue{Key:KUBERNETES_SERVICE_PORT,Value:443,},&KeyValue{Key:KUBERNETES_PORT,Value:tcp://10.96.0.1:443,},&KeyValue{Key:KUBERNETES_PORT_443_TCP_PORT,Value:443,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_80_TCP_ADDR,Value:10.107.5.252,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_SERVICE_HOST,Value:10.107.5.252,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_SERVICE_PORT,Value:80,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_SERVICE_PORT_SERVICE_PORT,Value:80,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_SERVICE_PORT_ZMQ_PORT,Value:55555,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_80_TCP,Value:tcp://10.107.5.252:80,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_80_TCP_PORT,Value:80,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_9999_TCP_PORT,Value:9999,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_SERVICE_PORT_UCX_PORT,Value:9999,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_55555_TCP_PORT,Value:55555,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_55555_TCP_ADDR,Value:10.107.5.252,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_9999_TCP,Value:tcp://10.107.5.252:9999,},&KeyValue{Key:KUBERNETES_SERVICE_HOST,Value:10.96.0.1,},&KeyValue{Key:KUBERNETES_SERVICE_PORT_HTTPS,Value:443,},&KeyValue{Key:KUBERNETES_PORT_443_TCP_PROTO,Value:tcp,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_55555_TCP,Value:tcp://10.107.5.252:55555,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT,Value:tcp://10.107.5.252:80,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_80_TCP_PROTO,Value:tcp,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_9999_TCP_PROTO,Value:tcp,},&KeyValue{Key:KUBERNETES_PORT_443_TCP,Value:tcp://10.96.0.1:443,},&KeyValue{Key:KUBERNETES_PORT_443_TCP_ADDR,Value:10.96.0.1,},&KeyValue{Key:EAPEBV9W9L_GRANITE_3_2_2B_INSTRUCT_ENGINE_SERVICE_PORT_55555_TCP_PROTO,Value:tcp,},},Mounts:[]*Mount{&Mount{ContainerPath:/var/run/secrets/kubernetes.io/serviceaccount,HostPath:/var/lib/kubelet/pods/1dbf314f-cf74-4181-8e4d-2aa0599d79c3/volumes/kubernetes.io~projected/kube-api-access-j4tlw,Readonly:true,SelinuxRelabel:false,Propagation:PROPAGATION_PRIVATE,UidMappings:[]*IDMapping{},GidMappings:[]*IDMapping{},RecursiveReadOnly:false,Image:nil,},&Mount{ContainerPath:/etc/hosts,HostPath:/var/lib/kubelet/pods/1dbf314f-cf74-4181-8e4d-2aa0599d79c3/etc-hosts,Readonly:false,SelinuxRelabel:false,Propagation:PROPAGATION_PRIVATE,UidMappings:[]*IDMapping{},GidMappings:[]*IDMapping{},RecursiveReadOnly:false,Image:nil,},&Mount{ContainerPath:/dev/termination-log,HostPath:/var/lib/kubelet/pods/1dbf314f-cf74-4181-8e4d-2aa0599d79c3/containers/vllm/6ff93535,Readonly:false,SelinuxRelabel:false,Propagation:PROPAGATION_PRIVATE,UidMappings:[]*IDMapping{},GidMappings:[]*IDMapping{},RecursiveReadOnly:false,Image:nil,},},Devices:[]*Device{&Device{ContainerPath:/dev/nvidiactl,HostPath:/dev/nvidiactl,Permissions:rw,},&Device{ContainerPath:/dev/nvidia-uvm,HostPath:/dev/nvidia-uvm,Permissions:rw,},&Device{ContainerPath:/dev/nvidia-uvm-tools,HostPath:/dev/nvidia-uvm-tools,Permissions:rw,},&Device{ContainerPath:/dev/nvidia-modeset,HostPath:/dev/nvidia-modeset,Permissions:rw,},&Device{ContainerPath:/dev/nvidia0,HostPath:/dev/nvidia0,Permissions:rw,},},Labels:map[string]string{io.kubernetes.container.name: vllm,io.kubernetes.pod.name: eapebv9w9l-granite-3-2-2b-instruct-deployment-vllm-ff445b7fzht2,io.kubernetes.pod.namespace: default,io.kubernetes.pod.uid: 1dbf314f-cf74-4181-8e4d-2aa0599d79c3,},Annotations:map[string]string{io.kubernetes.container.hash: d3768701,io.kubernetes.container.ports: [{"name":"container-port","containerPort":8000,"protocol":"TCP"},{"name":"zmq-port","containerPort":55555,"protocol":"TCP"},{"name":"ucx-port","containerPort":9999,"protocol":"TCP"}],io.kubernetes.container.restartCount: 0,io.kubernetes.container.terminationMessagePath: /dev/termination-log,io.kubernetes.container.terminationMessagePolicy: File,io.kubernetes.pod.terminationGracePeriod: 30,},LogPath:vllm/0.log,Stdin:false,StdinOnce:false,Tty:false,Linux:&LinuxContainerConfig{Resources:&LinuxContainerResources{CpuPeriod:100000,CpuQuota:0,CpuShares:6144,MemoryLimitInBytes:0,OomScoreAdj:912,CpusetCpus:,CpusetMems:,HugepageLimits:[]*HugepageLimit{&HugepageLimit{PageSize:2MB,Limit:0,},&HugepageLimit{PageSize:1GB,Limit:0,},},Unified:map[string]string{memory.oom.group: 1,memory.swap.max: 0,},MemorySwapLimitInBytes:0,},SecurityContext:&LinuxContainerSecurityContext{Capabilities:nil,Privileged:false,NamespaceOptions:&NamespaceOption{Network:POD,Pid:CONTAINER,Ipc:POD,TargetId:,UsernsOptions:nil,},SelinuxOptions:nil,RunAsUser:&Int64Value{Value:0,},RunAsUsername:,ReadonlyRootfs:false,SupplementalGroups:[],ApparmorProfile:,SeccompProfilePath:,NoNewPrivs:false,RunAsGroup:nil,MaskedPaths:[/proc/asound /proc/acpi /proc/kcore /proc/keys /proc/latency_stats /proc/timer_list /proc/timer_stats /proc/sched_debug /proc/scsi /sys/firmware /sys/devices/virtual/powercap],ReadonlyPaths:[/proc/bus /proc/fs /proc/irq /proc/sys /proc/sysrq-trigger],Seccomp:&SecurityProfile{ProfileType:Unconfined,LocalhostRef:,},Apparmor:nil,SupplementalGroupsPolicy:Merge,},},Windows:nil,CDIDevices:[]*CDIDevice{},}
```

Zoom into the head of `ContainerConfig.Envs`:
```
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

## What if null/zero specified in Resources

I tried to specify null values, i.e. delete `nvidia.com/gpu` from `PodSpec.Container.Resources`.
I also tried to specify zero values, i.e. set `nvidia.com/gpu: "0"` in `PodSpec.Container.Resources`.

I didn't find differences between these two cases when I was observing the `ContainerConfig` that is consumed by the gRPC call. So I will treat them as one case 'null/zero' in this section.

For the 'null/zero' case:
- The 1st instance of the `NVIDIA_VISIBLE_DEVICES` envar disappears from `ContainerConfig.Envs`;
- GPU(s) `/dev/nvidiaX` are not injected into `ContainerConfig.Mounts`;
- 'Supportive' devices such as `/dev/nvidiactl`, `/dev/nvidia-uvm`, `/dev/nvidia-uvm-tools`, `/dev/nvidia-modeset` are not injected into `ContainerConfig.Mounts`.

For the 'null/zero' case, if `NVIDIA_VISIBLE_DEVICES` is specified in `PodSpec.Container.Env`:
- The 2nd instance of the `NVIDIA_VISIBLE_DEVICES` envar stays in `ContainerConfig.Envs`;
- The vLLM pod is able to run using the GPU(s) specified by the 2nd instance of the envar.

For the 'null/zero' case, if `NVIDIA_VISIBLE_DEVICES` is not specified in `PodSpec.Container.Env`:
- The 2nd instance of the `NVIDIA_VISIBLE_DEVICES` envar disappears from `ContainerConfig.Envs`;
- The vLLM pod is able to see all GPU(s).

## Check the nvidia container toolkit
There are two interesting components in the nvidia container toolkit.

### The nvidia container runtime hook
The nvidia container runtime hook is invoked by runc, 'after a container has been created, but before it has been started'.

One statement in [nvidia doc](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/arch-overview.html) is:

> It (nvidia container runtime hook) then takes information contained in the config.json and uses it to invoke the nvidia-container-cli CLI with an appropriate set of flags. One of the most important flags being which specific GPU devices should be injected into the container.

### The nvidia container cli
The nvidia container cli is called by the nvidia container runtime hook.

One line of [nvidia container runtime code](https://github.com/NVIDIA/nvidia-container-toolkit/blob/08b3a388e7b1d447e10d4c4d4a71dca29a98a964/cmd/nvidia-container-runtime/README.md?plain=1#L91) says:

> Each environment variable maps to a command-line argument...

OK 'each' envar and yes I [tried](https://github.com/NVIDIA/nvidia-container-toolkit/pull/1257) to fix the typo.
But what happens if there are two *instances* of *one* `NVIDIA_VISIBLE_DEVICES` envar?

## Conclusions
- I suspect some other entity has duplicated functionality with the (kubelet, device plugin) pair,
in terms of mounting the GPU(s) and supportive devices into the container.
- I suspect that entity is (part of) the nvidia container toolkit.
- I suspect this duplication is the source of our GPU assignment problem.
