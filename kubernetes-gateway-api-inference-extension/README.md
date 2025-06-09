This is a hands-on experiment of the Kubernetes Gateway API Inference Extension.
The experiment is based on this [article](https://mp.weixin.qq.com/s/WflalqTE0c-_mYUsEmMiRA).

The YAML files used in this experiments are based on [these](https://github.com/cr7258/hands-on-lab/tree/414445dfd2ab58a7310bd385f2bbf13dca1d76a3/gateway/gateway-api-inference-extension/get-started).
I didn't fork that repostory because it's too large and it has many other contents that are not related to this experiment.
I made some changes to the YAMLs to fix minor mistakes and to fit it into my tiny testbed.

As a prerequisite, I installed the Kubernetes Gateway API (i.e. CRDs). This prerequisite not explicitly mentioned in the article.
```
kubectl apply -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
```
by following [k8s doc](https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml)

## Steps
```
kubectl create -f kubernetes-gateway-api-inference-extension/04-gateway.yaml
```
After the creation of the Gateway `inference-gateway`, a Depolyment also named `inference-gateway` is created by kgateway.
The Deployment has a owner reference to the Gateway.

```
{"level":"info","ts":"2025-06-09T16:19:28Z","logger":"kgateway","msg":"reconciling gateway","version":"v2.0.0","controller":"gateway","controllerGroup":"gateway.networking.k8s.io","controllerKind":"Gateway","Gateway":{"name":"inference-gateway","namespace":"default"},"namespace":"default","name":"inference-gateway","reconcileID":"d86cff55-0ad4-459d-9bd6-6ade72e9db6a","gw":{"name":"inference-gateway","namespace":"default"}}
```

My gateway doesn't have an address
```
kubectl get gateway
NAME                CLASS      ADDRESS   PROGRAMMED   AGE
inference-gateway   kgateway             True         37m
```
But I can use the Cluster-IP of the 'inference-gateway' service as the address.
```
$ kubectl get svc
NAME                          TYPE           CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
inference-gateway             LoadBalancer   10.106.190.166   <pending>     80:31437/TCP   38m
kubernetes                    ClusterIP      10.96.0.1        <none>        443/TCP        93d
vllm-llama3-3b-instruct-epp   ClusterIP      10.109.18.70     <none>        9002/TCP       45m
```

```
curl -i ${IP}:${PORT}/v1/completions -H 'Content-Type: application/json' -d '{
"model": "news",
"prompt": "Write as if you were a critic: San Francisco",
"max_tokens": 100,
"temperature": 0
}'
```

```
curl 10.0.0.150:80/v1/models
```

## Cleaning up
```
kubectl delete -f kubernetes-gateway-api-inference-extension/05-httproute.yaml
kubectl delete -f kubernetes-gateway-api-inference-extension/04-gateway.yaml

helm -n kgateway-system uninstall kgateway
helm -n kgateway-system uninstall kgateway-crd
kubectl delete ns kgateway-system

kubectl delete -f kubernetes-gateway-api-inference-extension/03-inferencepool-resources.yaml

kubectl delete -f kubernetes-gateway-api-inference-extension/02-inferencemodel.yaml

GIE_VERSION=v0.2.0
kubectl delete -f https://github.com/kubernetes-sigs/gateway-api-inference-extension/releases/download/$GIE_VERSION/manifests.yaml

kubectl delete -f kubernetes-gateway-api-inference-extension/01-gpu-deployment.yaml

kubectl delete secret hf-token

kubectl delete -f https://github.com/kubernetes-sigs/gateway-api/releases/download/v1.3.0/standard-install.yaml
```