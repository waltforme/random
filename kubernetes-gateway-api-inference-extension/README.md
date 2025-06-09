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
My gateway doesn't have an address
```
kc get gateway
NAME                CLASS      ADDRESS   PROGRAMMED   AGE
inference-gateway   kgateway             True         37m
```
But I can use the Cluster-IP of the 'inference-gateway' service as the address.
```
$ kc get svc
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
