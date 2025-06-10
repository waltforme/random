This is a hands-on experiment of the Kubernetes Gateway API Inference Extension (GIE).
The experiment setup a vLLM instance using the meta-llama/Llama-3.2-3B-Instruct model and two LoRA adapters,
then demonstrates a grayscale release of models using the Inference Extension.

The experiment is based on this [article](https://mp.weixin.qq.com/s/WflalqTE0c-_mYUsEmMiRA).
The YAML files used in this experiments are based on [these](https://github.com/cr7258/hands-on-lab/tree/414445dfd2ab58a7310bd385f2bbf13dca1d76a3/gateway/gateway-api-inference-extension/get-started).
I didn't fork that repostory because it's too large and it has many other contents that are not related to this experiment.
I made some changes to the YAML files to fix minor mistakes and to fit it into my tiny testbed.

The hardware used by this experiment is an AWS EC2 instance of type g6.4xlarge, which has a nVidia L4 GPU.
A single-node Kubernetes v1.32.2 cluster is installed by kubeadm on top of the EC2 instance.

As a prerequisite, I installed the Kubernetes Gateway API (i.e. CRDs)
by following [k8s doc](https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml)
```shell
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
```
This prerequisite is not explicitly mentioned in the article.

## Setup
1. Create a Secret for Hugging Face token.
```shell
kubectl create secret generic hf-token --from-literal=token="<my-huggingface-token>"
```

2. Create a Deployment for the vLLM instance and a ConfigMap for LoRA configurations.
```shell
kubectl create -f ./kubernetes-gateway-api-inference-extension/01-gpu-deployment.yaml
```
Check logs of the vLLM instance.
```shell
kubectl logs deploy/01-gpu-deployment.yaml
```

3. Install the GIE CRDs.
```shell
GIE_VERSION=v0.2.0
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api-inference-extension/releases/download/$GIE_VERSION/manifests.yaml
```

4. Create the InferenceModel.
```shell
kubectl create -f ./kubernetes-gateway-api-inference-extension/02-inferencemodel.yaml
```

5. Create resources for the InferencePool, the Endpoint Picker (EPP), and RBAC.
```shell
kubectl create -f ./kubernetes-gateway-api-inference-extension/03-inferencepool-resources.yaml
```

6. Install the kgateway CRDS and the kgateway controller.
```shell
KGTW_VERSION=v2.0.0
helm upgrade -i --create-namespace --namespace kgateway-system --version $KGTW_VERSION kgateway-crds oci://cr.kgateway.dev/kgateway-dev/charts/kgateway-crds
helm upgrade -i --namespace kgateway-system --version $KGTW_VERSION kgateway oci://cr.kgateway.dev/kgateway-dev/charts/kgateway --set inferenceExtension.enabled=true
```

7. Create the Gateway.
```shell
kubectl create -f ./kubernetes-gateway-api-inference-extension/04-gateway.yaml
```

After creation of the Gateway `inference-gateway`, a Depolyment also named `inference-gateway` is created by kgateway.
The Deployment has a owner reference to the Gateway.
```console
{"level":"info","ts":"2025-06-09T16:19:28Z","logger":"kgateway","msg":"reconciling gateway","version":"v2.0.0","controller":"gateway","controllerGroup":"gateway.networking.k8s.io","controllerKind":"Gateway","Gateway":{"name":"inference-gateway","namespace":"default"},"namespace":"default","name":"inference-gateway","reconcileID":"d86cff55-0ad4-459d-9bd6-6ade72e9db6a","gw":{"name":"inference-gateway","namespace":"default"}}
```

My gateway doesn't have an address.
```console
kubectl get gateway
NAME                CLASS      ADDRESS   PROGRAMMED   AGE
inference-gateway   kgateway             True         37m
```

But I can use the Cluster-IP of the `inference-gateway` service as the address in the rest of the experiment.
```console
$ kubectl get svc
NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
inference-gateway             LoadBalancer   10.99.83.145     <pending>     80:32693/TCP   38s
kubernetes                    ClusterIP      10.96.0.1        <none>        443/TCP        95d
vllm-llama3-3b-instruct-epp   ClusterIP      10.102.143.160   <none>        9002/TCP       2m8s
$ GW_IP=10.99.83.145
$ GW_PORT=80
```

8. Create the HTTPRoute.
```shell
kubectl create -f ./kubernetes-gateway-api-inference-extension/05-httproute.yaml
```

## Grayscale release
```shell
curl -i ${GW_IP}:${GW_PORT}/v1/completions -H 'Content-Type: application/json' -d '{
  "model": "news",
  "prompt": "Write as if you were a critic: San Francisco",
  "max_tokens": 100,
  "temperature": 0
}'
```

```shell
curl -s ${GW_IP}:${GW_PORT}/v1/models | jq
```

## Cleaning up
Cleaning up is the reverse of the Setup.
```shell
kubectl delete -f ./kubernetes-gateway-api-inference-extension/05-httproute.yaml
kubectl delete -f ./kubernetes-gateway-api-inference-extension/04-gateway.yaml

helm -n kgateway-system uninstall kgateway
helm -n kgateway-system uninstall kgateway-crd
kubectl delete ns kgateway-system

kubectl delete -f ./kubernetes-gateway-api-inference-extension/03-inferencepool-resources.yaml

kubectl delete -f ./kubernetes-gateway-api-inference-extension/02-inferencemodel.yaml

GIE_VERSION=v0.2.0
kubectl delete -f https://github.com/kubernetes-sigs/gateway-api-inference-extension/releases/download/$GIE_VERSION/manifests.yaml

kubectl delete -f ./kubernetes-gateway-api-inference-extension/01-gpu-deployment.yaml

kubectl delete secret hf-token

kubectl delete -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
```