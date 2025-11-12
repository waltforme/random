This document mainly discusses the relationship between the llm-d-fast-model-actuation ('FMA') project and
the Kubernetes Gateway API Inference Extension (GIE).

The main question is, whether FMA should be in charge of managing the lifecycle of GIE objects (technically, it's Gateway *and* GIE objects because httproutes' API group is `gateway.networking.k8s.io` and inferencepools' API group is `inference.networking.x-k8s.io`), such as httproutes, inferencepools, and endpoint pickers (EPPs).

Some related questions are also discussed.

## The short answer
Generally, no.

As a rule of thumb, infrastructure and workload should be managed separately.
In the context of llm-d, GIE objects are infrastructure, and the vLLM instances are workloads.

FMA's interest, as its name suggests, is primarily about speeding up the start of vLLM engines.
Or more concretely, minimizing TTFT using whatever available technology with the constraint of limited GPUs.
Therefore, FMA's scope is about managing workloads.
FMA should not take the responsibility to manage the lifecycle of infrastructure objects.


## The long answer
So what is the community's common practice to manage the infrastructure?
Some investigation shows that the answer is helm/helmfile.

- llm-d/llm-d: helmfile
- llm-d/llm-d-benchmark helmfile
- llm-d-incubation/llm-d-infra: helmfile
- llm-d-incubation/llm-d-modelservice: helm

Note that in the list above, the setups are minimized in terms of number of models.
They are minimized because the setups are mostly guides/tutorials/tests, not production deployments.
What if the number scale out? This question leads to the next discussion.


## Optimization?
Could there be optimizations of the infrastructure when the number of models increases?

It is commonly seen that there is a 1:1:1 mapping between models, inferencepools, and EPPs.
Speaking of optimization, does it make sense that
1. multiple models share one inferencepool?
2. multiple inferencepools share one EPP?

AFAIK, answers to the two questions unfortunately are both 'no', detailed as follows.


### 1:1 mapping between models and inferencepools
I did some experiments, trying to make two models to share one inference pool.

I started from the llm-d/llm-d [guide to 'Intelligent Inference Scheduling'](https://github.com/llm-d/llm-d/tree/main/guides/inference-scheduling).

One InferencePool object was created.
```console
👉 tmp $ oc get xinfpool gaie-inference-scheduling -oyaml | yq .spec
extensionRef:
  failureMode: FailClose
  group: ""
  kind: Service
  name: gaie-inference-scheduling-epp
  portNumber: 9002
selector:
  llm-d.ai/inferenceServing: "true"
targetPortNumber: 8000
```

On top of the successfully installation, I manually added another Deployment which serves `ibm-granite/granite-3.3-2b-instruct` by `vllm/vllm-openai:v0.10.2`.
Then I labeled the corresponding pod to associate the pod with the InferencePool object.
```shell
oc label po gpu-placeholder-76dd8d4c64-mktn8 llm-d.ai/inferenceServing=true
```

I sent inference requests to the default model of the guide, `Qwen/Qwen3-0.6B`,
and got mixed responses of 404 and correct completions.
```console
👉 tmp $ curl -s -X POST ${ENDPOINT}/v1/completions \
>   -H 'Content-Type: application/json' \
>   -d '{
>         "model": "Qwen/Qwen3-0.6B",
>         "prompt": "Which large language model is used by you? "
>       }' | jq
{
  "error": {
    "code": 404,
    "message": "The model `Qwen/Qwen3-0.6B` does not exist.",
    "param": null,
    "type": "NotFoundError"
  }
}
👉 tmp $ curl -s -X POST ${ENDPOINT}/v1/completions \
>   -H 'Content-Type: application/json' \
>   -d '{
>         "model": "Qwen/Qwen3-0.6B",
>         "prompt": "Which large language model is used by you? "
>       }' | jq
{
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "logprobs": null,
      "prompt_logprobs": null,
      "prompt_token_ids": null,
      "stop_reason": null,
      "text": " - A. BERT  - B. RoBERT  - C. B",
      "token_ids": null
    }
  ],
  "created": 1762831297,
  "id": "cmpl-2d564794-3a7c-4f4e-801f-baf9abdab236",
  "kv_transfer_params": null,
  "model": "Qwen/Qwen3-0.6B",
  "object": "text_completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 16,
    "prompt_tokens": 10,
    "prompt_tokens_details": null,
    "total_tokens": 26
  }
}
```

Similarly, I sent inference requests to `ibm-granite/granite-3.3-2b-instruct`,
and got mixed responses of 404 and correct completions.
```console
👉 tmp $ curl -s -X POST ${ENDPOINT}/v1/completions   -H 'Content-Type: application/json'   -d '{
        "model": "ibm-granite/granite-3.3-2b-instruct",
        "prompt": "Which large language model is used by you? "
      }' | jq
{
  "error": {
    "code": 404,
    "message": "The model `ibm-granite/granite-3.3-2b-instruct` does not exist.",
    "param": null,
    "type": "NotFoundError"
  }
}
👉 tmp $ curl -s -X POST ${ENDPOINT}/v1/completions   -H 'Content-Type: application/json'   -d '{
        "model": "ibm-granite/granite-3.3-2b-instruct",
        "prompt": "Which large language model is used by you? "
      }' | jq
{
  "choices": [
    {
      "finish_reason": "length",
      "index": 0,
      "logprobs": null,
      "prompt_logprobs": null,
      "prompt_token_ids": null,
      "stop_reason": null,
      "text": " How does it differ from a typical language model?\n\nA large language model",
      "token_ids": null
    }
  ],
  "created": 1762831240,
  "id": "cmpl-da88b856-b8e7-4144-877b-f927197633be",
  "kv_transfer_params": null,
  "model": "ibm-granite/granite-3.3-2b-instruct",
  "object": "text_completion",
  "service_tier": null,
  "system_fingerprint": null,
  "usage": {
    "completion_tokens": 16,
    "prompt_tokens": 10,
    "prompt_tokens_details": null,
    "total_tokens": 26
  }
}
```

Here is the hypothesis.
My inference requests are dispatched to the two vLLM pods because both pods are associated with the InferencePool object.
But the two pods serves different models.
If an inference request is dispatched to the pod which serves the model that the request asks for, the request is fulfilled.
Otherwise, a 404 is returned.

To verify that.
I sent a bunch of (39) inference requests to `Qwen/Qwen3-0.6B`,
followed by a bunch of (49) inference requests to `ibm-granite/granite-3.3-2b-instruct`,
and meanwhile watched the logs of both of the vLLM pods.

Logs of the pod which serves `Qwen/Qwen3-0.6B`:
```console
👉 tmp $ oc logs deploy/ms-inference-scheduling-llm-d-modelservice-decode --tail 10 -f | grep POST
Defaulted container "vllm" out of: vllm, routing-proxy (init)
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:0 - "POST /v1/completions HTTP/1.1" 404 Not Found
```

Logs of the pod which serves `ibm-granite/granite-3.3-2b-instruct`:
```console
👉 tmp $ oc logs deploy/gpu-placeholder --tail 10 -f | grep POST
(APIServer pid=1) INFO:     10.130.7.103:45668 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:33648 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:33656 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:44942 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:53204 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:53212 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:53226 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:42894 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:42904 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:42918 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41726 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41742 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41758 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41770 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41784 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:41794 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:54802 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:54818 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:54820 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:54822 - "POST /v1/completions HTTP/1.1" 404 Not Found
(APIServer pid=1) INFO:     10.130.7.103:36878 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:54806 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:54814 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33758 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33770 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33784 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33792 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33800 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:33806 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:40872 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:40886 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:40902 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:40918 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:40920 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46688 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46692 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46706 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46708 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46720 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46736 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46742 - "POST /v1/completions HTTP/1.1" 200 OK
(APIServer pid=1) INFO:     10.130.7.103:46756 - "POST /v1/completions HTTP/1.1" 200 OK
^C
```

A few observations:
- 39 requests asked for `Qwen/Qwen3-0.6B`, where 19 were dispatched correctly, 20 were not and (so 404).
- 49 requests asked for `ibm-granite/granite-3.3-2b-instruct`, where 27 were dispatched correctly, 22 were not (so 404).
- 46 inference requests were dispatched to the pod which serves `Qwen/Qwen3-0.6B`,
- 42 inference requests were dispatched to the pod which serves `ibm-granite/granite-3.3-2b-instruct`.

So the hypothesis is confirmed. To repeat the hypothesis:
If an inference request is dispatched to the pod which serves the model that the request asks for, the request is fulfilled.
Otherwise, a 404 is returned.

Since inference requests are dispatched to all pods that are associated with an InferencePool object,
the pods must serve the same model (otherwise 404).
In other words, different models can not share one InferencePool object (thus 1:1).

### 1:1 mapping between inferencepools and EPPs
I checked one EPP pod:
```console
👉 tmp $ oc get po gaie-inference-scheduling-epp-669895bf4d-tjqjb -oyaml | yq .spec.containers
- args:
    - --pool-name
    - gaie-inference-scheduling
    - --pool-namespace
    - fma-dev
    - --pool-group
    - inference.networking.x-k8s.io
    - --zap-encoder
    - json
    - --config-file
    - /config/default-plugins.yaml
    - --v
    - "1"
  env:
    - name: NAMESPACE
      valueFrom:
        fieldRef:
          apiVersion: v1
          fieldPath: metadata.namespace
  image: ghcr.io/llm-d/llm-d-inference-scheduler:v0.3.2
  imagePullPolicy: Always
  livenessProbe:
    failureThreshold: 3
    grpc:
      port: 9003
      service: inference-extension
    initialDelaySeconds: 5
    periodSeconds: 10
    successThreshold: 1
    timeoutSeconds: 1
  name: epp
  ports:
    - containerPort: 9002
      name: grpc
      protocol: TCP
    - containerPort: 9003
      name: grpc-health
      protocol: TCP
    - containerPort: 9090
      name: metrics
      protocol: TCP
  readinessProbe:
    failureThreshold: 3
    grpc:
      port: 9003
      service: inference-extension
    periodSeconds: 2
    successThreshold: 1
    timeoutSeconds: 1
  resources: {}
  securityContext:
    allowPrivilegeEscalation: false
    capabilities:
      drop:
        - ALL
    runAsNonRoot: true
    runAsUser: 1001480000
  terminationMessagePath: /dev/termination-log
  terminationMessagePolicy: File
  volumeMounts:
    - mountPath: /config
      name: plugins-config-volume
    - mountPath: /var/run/secrets/kubernetes.io/serviceaccount
      name: kube-api-access-fplf2
      readOnly: true
```

I see an EPP container ties itself to exactly one InferencePool object by specifiying the namespace and name of that object.
In other words, the EPP container can't handle more than one InferencePool object.

To double check, I checked the EPP's code see that
1. the name of the InferencePool object is a required flag:
https://github.com/kubernetes-sigs/gateway-api-inference-extension/blob/7488c2b0b3a43e28fc7bd684256d67ce848fda28/cmd/epp/runner/runner.go#L569

2. the namespace must take some concrete value:
https://github.com/kubernetes-sigs/gateway-api-inference-extension/blob/7488c2b0b3a43e28fc7bd684256d67ce848fda28/cmd/epp/runner/runner.go#L244-L258

So, multiple InferencePool objects can not share an EPP pod (thus 1:1).


## Are there collisions/overlapped functions between the dpctlr and the EPP?
This question concerns about the optimization within a model.
Writing to be finished.
