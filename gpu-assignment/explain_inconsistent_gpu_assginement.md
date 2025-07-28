In our recent LLM inferencing use case, we tried to assign a specific set of GPUs to vLLM, instead of merely assign 'how many' GPUs.
We tried to use the `NVIDIA_VISIBLE_DEVICES` environment variable in the `PodSpec.Container.Env` of vLLM Deployment to achieve the goal.
But the running vLLM container usually saw more GPU than we specified by `NVIDIA_VISIBLE_DEVICES`.

This short experiment explains why the actually seen GPUs are inconsistent with what specified by `NVIDIA_VISIBLE_DEVICES`.

**The root cause of the inconsistency is that the device plugin consumes `PodSpec.Container.Resources` and accordingly recommends an allocation to the kubelet,
then both the `PodSpec.Container.Env` specified GPUs and the `PodSpec.Container.Resources`-based allocation are honored.**

There are four GPUs in the node of my test setup.
```console
$ nvidia-smi --query-gpu=index,uuid,memory.used --format=csv
index, uuid, memory.used [MiB]
0, GPU-d7082db6-9ee4-f65a-bf86-3319f528ba4d, 20748 MiB
1, GPU-3d75cdd5-2ceb-76a5-8462-d3c24394fdcd, 3 MiB
2, GPU-38c3274b-3405-73ce-59d4-8a66e285047f, 0 MiB
3, GPU-2036c212-60d9-ce87-6017-f587f33db900, 0 MiB
```

A vLLM pod specified GPU 1 by the `NVIDIA_VISIBLE_DEVICES` environment variable in its `PodSpec.Container.Env`.
```consolev
$ kc get deploy ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm -o jsonpath='{range .spec.template.spec.containers[*].env[*]}{.name}={.value}{"\n"}{end}'
HF_HOME=/tmp
POD_IP=
LMCACHE_LOG_LEVEL=DEBUG
NVIDIA_VISIBLE_DEVICES=1
VLLM_SERVER_DEV_MODE=1
VLLM_USE_V1=1
```

The vLLM container saw two GPUs, with an extra GPU in addition to the specified one.
```console
$ kc exec deploy/ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm -- nvidia-smi --query-gpu=index,uuid,memory.used --format=csv
index, uuid, memory.used [MiB]
0, GPU-d7082db6-9ee4-f65a-bf86-3319f528ba4d, 20748 MiB
1, GPU-3d75cdd5-2ceb-76a5-8462-d3c24394fdcd, 3 MiB
```

Mdified kubelet unveils that the extra GPU was recommended by the device plugin and adopted by kubelet.
```text
MyDebug(show PreferredAllocationResponse): &PreferredAllocationResponse{ContainerResponses:[]*ContainerPreferredAllocationResponse{&ContainerPreferredAllocationResponse{DeviceIDs:[GPU-d7082db6-9ee4-f65a-bf86-3319f528ba4d],},},}
MyDebug(show allocDevices): map[GPU-d7082db6-9ee4-f65a-bf86-3319f528ba4d:{}]
MyDebug(show AllocateResponse): &AllocateResponse{ContainerResponses:[]*ContainerAllocateResponse{&ContainerAllocateResponse{Envs:map[string]string{NVIDIA_VISIBLE_DEVICES: GPU-d7082db6-9ee4-f65a-bf86-3319f528ba4d,},Mounts:[]*Mount{},Devices:[]*DeviceSpec{&DeviceSpec{ContainerPath:/dev/nvidiactl,HostPath:/dev/nvidiactl,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-uvm,HostPath:/dev/nvidia-uvm,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-uvm-tools,HostPath:/dev/nvidia-uvm-tools,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia-modeset,HostPath:/dev/nvidia-modeset,Permissions:rw,},&DeviceSpec{ContainerPath:/dev/nvidia0,HostPath:/dev/nvidia0,Permissions:rw,},},Annotations:map[string]string{},CDIDevices:[]*CDIDevice{},},},}
```

Why the inconsistency exists:
- vLLM Pod specifed GPU 1;
- device plugin recommended GPU 0;
- kubelet allocated GPU 0;
- both GPUs were made accessible for the vLLM container;
- GPU 0 picked up by vLLM container, instead of the `PodSpec.Container.Env`-specified GPU 1.

Make the assignment consistent.
```console
$ kc scale deploy ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm --replicas=0
deployment.apps/ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm scaled
$ kc get deployment ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm -o jsonpath="{.spec.template.spec.containers[*].resources}" | jq
{
  "limits": {
    "nvidia.com/gpu": "1"
  },
  "requests": {
    "cpu": "6",
    "memory": "16Gi",
    "nvidia.com/gpu": "1"
  }
}
$ kc edit deploy ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm
deployment.apps/ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm edited
$ kc get deployment ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm -o jsonpath="{.spec.template.spec.containers[*].resources}" | jq
{
  "requests": {
    "cpu": "6",
    "memory": "16Gi"
  }
}
$ kc scale deploy ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm --replicas=1
deployment.apps/ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm scaled
```

(No more log from modified kubelet)

```console
$ kc exec deploy/ubkn3zm1o6-granite-3-2-2b-instruct-deployment-vllm -- nvidia-smi --query-gpu=index,uuid,memory.used --format=csv
index, uuid, memory.used [MiB]
0, GPU-3d75cdd5-2ceb-76a5-8462-d3c24394fdcd, 20748 MiB
```

In this consistent assignment:
- Pod specified GPU 1;
- device plugin not involved;
- GPU 1 was solely made accessible for the vLLM container as specified.

Why device plugin was not involved again? Let's look at a kubelet code snippet and my changed comment:
```txt
@@ -832,7 +832,10 @@ func (m *ManagerImpl) allocateContainerResources(pod *v1.Pod, container *v1.Cont
        // Extended resources are not allowed to be overcommitted.
        // Since device plugin advertises extended resources,
        // therefore Requests must be equal to Limits and iterating
-       // over the Limits should be sufficient.
+       // over the Limits should be sufficient in the sense that Requests can be ignored,
+       // but actually not sufficient when user wants not just 'how many devices' but also 'which devices'
+       // e.g. in our use case.
+       // So improvements can be made here to consider user specified NVIDIA_VISIBLE_DEVICES before using the plugin.
        for k, v := range container.Resources.Limits {
                resource := string(k)
                needed := int(v.Value())
```

As commented, there might be some oppotunity here to contribute a feature to define/reconcile the relationship between
- the user specified `NVIDIA_VISIBLE_DEVICES` in `PodSpec.Container.Env`, and
- the user specified requests and limits for 'nvdia.com/gpu' in `PodSpec.Container.Resources`,

so that more fine-grained control --- assigning a specific set of GPUs --- can be offered to the user.

I'm not sure where the contribution should go though. Going into kubelet sounds like a violation of modularity. Maybe into the consumer of the kubelet-processed PodSpec which sould be nvidia container runtime?
