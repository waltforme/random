Create a Deploymet object.
```console
kubectl create -f nginx-0930.yaml
deployment.apps/nginx-0930 created
```

Check the managedFields. The object has a single owner which is `kubectl-create`.
```console
kubectl get deploy nginx-0930 -oyaml --show-managed-fields | yq .metadata.managedFields
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:metadata:
      f:labels:
        .: {}
        f:app: {}
    f:spec:
      f:progressDeadlineSeconds: {}
      f:replicas: {}
      f:revisionHistoryLimit: {}
      f:selector: {}
      f:strategy:
        f:rollingUpdate:
          .: {}
          f:maxSurge: {}
          f:maxUnavailable: {}
        f:type: {}
      f:template:
        f:metadata:
          f:labels:
            .: {}
            f:app: {}
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              .: {}
              f:image: {}
              f:imagePullPolicy: {}
              f:name: {}
              f:resources: {}
              f:terminationMessagePath: {}
              f:terminationMessagePolicy: {}
          f:dnsPolicy: {}
          f:restartPolicy: {}
          f:schedulerName: {}
          f:securityContext: {}
          f:terminationGracePeriodSeconds: {}
  manager: kubectl-create
  operation: Update
  time: "2024-09-30T19:31:32Z"
```

`kubectl patch` the object, to change the image tag from `mainline` to `stable`.
```console
kubectl patch deployment nginx-0930 \
    --type='json' \
    -p='[
        {"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"nginx:stable"}
    ]' \
    -v 8
I0930 19:42:47.647929 1785205 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/managedfields/mypki/admin.kubeconfig
I0930 19:42:47.651178 1785205 round_trippers.go:463] GET https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930
I0930 19:42:47.651199 1785205 round_trippers.go:469] Request Headers:
I0930 19:42:47.651210 1785205 round_trippers.go:473]     Accept: application/json
I0930 19:42:47.651219 1785205 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 19:42:47.661176 1785205 round_trippers.go:574] Response Status: 200 OK in 9 milliseconds
I0930 19:42:47.661197 1785205 round_trippers.go:577] Response Headers:
I0930 19:42:47.661209 1785205 round_trippers.go:580]     Date: Mon, 30 Sep 2024 19:42:47 GMT
I0930 19:42:47.661216 1785205 round_trippers.go:580]     Audit-Id: 3d352bea-61f8-49ed-8433-1c18c3bc8c69
I0930 19:42:47.661223 1785205 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 19:42:47.661229 1785205 round_trippers.go:580]     Content-Type: application/json
I0930 19:42:47.661236 1785205 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 19:42:47.661243 1785205 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 19:42:47.661249 1785205 round_trippers.go:580]     Content-Length: 1672
I0930 19:42:47.661350 1785205 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5807ba64-97ff-4eb9-a044-a1ca9a361351","resourceVersion":"6409","generation":1,"creationTimestamp":"2024-09-30T19:31:32Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T19:31:32Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]}, [truncated 648 chars]
I0930 19:42:47.661634 1785205 request.go:1171] Request Body: [{"op":"replace","path":"/spec/template/spec/containers/0/image","value":"nginx:stable"}]
I0930 19:42:47.661672 1785205 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=kubectl-patch
I0930 19:42:47.661680 1785205 round_trippers.go:469] Request Headers:
I0930 19:42:47.661689 1785205 round_trippers.go:473]     Accept: application/json
I0930 19:42:47.661697 1785205 round_trippers.go:473]     Content-Type: application/json-patch+json
I0930 19:42:47.661705 1785205 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 19:42:47.666272 1785205 round_trippers.go:574] Response Status: 200 OK in 4 milliseconds
I0930 19:42:47.666291 1785205 round_trippers.go:577] Response Headers:
I0930 19:42:47.666309 1785205 round_trippers.go:580]     Content-Type: application/json
I0930 19:42:47.666317 1785205 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 19:42:47.666324 1785205 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 19:42:47.666331 1785205 round_trippers.go:580]     Content-Length: 1890
I0930 19:42:47.666337 1785205 round_trippers.go:580]     Date: Mon, 30 Sep 2024 19:42:47 GMT
I0930 19:42:47.666344 1785205 round_trippers.go:580]     Audit-Id: 2ef6e832-a92a-4fc3-a0c0-7fa1d438b37a
I0930 19:42:47.666350 1785205 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 19:42:47.666377 1785205 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5807ba64-97ff-4eb9-a044-a1ca9a361351","resourceVersion":"6545","generation":2,"creationTimestamp":"2024-09-30T19:31:32Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T19:31:32Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"kub [truncated 866 chars]
deployment.apps/nginx-0930 patched
```
We can see an HTTP PATCH is sent to apiserver.

Check the managedFields. The object has two owners, `kubectl-create` and `kubectl-patch`.
```console
kubectl get deploy nginx-0930 -oyaml --show-managed-fields | yq .metadata.managedFields
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:metadata:
      f:labels:
        .: {}
        f:app: {}
    f:spec:
      f:progressDeadlineSeconds: {}
      f:replicas: {}
      f:revisionHistoryLimit: {}
      f:selector: {}
      f:strategy:
        f:rollingUpdate:
          .: {}
          f:maxSurge: {}
          f:maxUnavailable: {}
        f:type: {}
      f:template:
        f:metadata:
          f:labels:
            .: {}
            f:app: {}
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              .: {}
              f:imagePullPolicy: {}
              f:name: {}
              f:resources: {}
              f:terminationMessagePath: {}
              f:terminationMessagePolicy: {}
          f:dnsPolicy: {}
          f:restartPolicy: {}
          f:schedulerName: {}
          f:securityContext: {}
          f:terminationGracePeriodSeconds: {}
  manager: kubectl-create
  operation: Update
  time: "2024-09-30T19:31:32Z"
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:spec:
      f:template:
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              f:image: {}
  manager: kubectl-patch
  operation: Update
  time: "2024-09-30T19:42:47Z"
```

`kubectl patch` the object again, to change the replicas from 1 to 2, as well as set the image tag to the already-set-as-same value `stable`.
```console
kubectl patch deployment nginx-0930 \
    --type='json' \
    -p='[
        {"op": "replace", "path": "/spec/template/spec/containers/0/image", "value":"nginx:stable"},
        {"op": "replace", "path": "/spec/replicas", "value": 2}
    ]' \
    --field-manager=kubectl-patch-again \
    -v 8
I0930 19:51:41.658846 1787965 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/managedfields/mypki/admin.kubeconfig
I0930 19:51:41.662422 1787965 round_trippers.go:463] GET https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930
I0930 19:51:41.662446 1787965 round_trippers.go:469] Request Headers:
I0930 19:51:41.662458 1787965 round_trippers.go:473]     Accept: application/json
I0930 19:51:41.662467 1787965 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 19:51:41.672435 1787965 round_trippers.go:574] Response Status: 200 OK in 9 milliseconds
I0930 19:51:41.672460 1787965 round_trippers.go:577] Response Headers:
I0930 19:51:41.672477 1787965 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 19:51:41.672485 1787965 round_trippers.go:580]     Content-Length: 1890
I0930 19:51:41.672492 1787965 round_trippers.go:580]     Date: Mon, 30 Sep 2024 19:51:41 GMT
I0930 19:51:41.672499 1787965 round_trippers.go:580]     Audit-Id: 06df4b16-9ec1-4be6-9ccd-d51d134d77e7
I0930 19:51:41.672505 1787965 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 19:51:41.672511 1787965 round_trippers.go:580]     Content-Type: application/json
I0930 19:51:41.672535 1787965 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 19:51:41.672575 1787965 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5807ba64-97ff-4eb9-a044-a1ca9a361351","resourceVersion":"6545","generation":2,"creationTimestamp":"2024-09-30T19:31:32Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T19:31:32Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"kub [truncated 866 chars]
I0930 19:51:41.672870 1787965 request.go:1171] Request Body: [{"op":"replace","path":"/spec/template/spec/containers/0/image","value":"nginx:stable"},{"op":"replace","path":"/spec/replicas","value":2}]
I0930 19:51:41.672907 1787965 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=kubectl-patch-again
I0930 19:51:41.672914 1787965 round_trippers.go:469] Request Headers:
I0930 19:51:41.672922 1787965 round_trippers.go:473]     Content-Type: application/json-patch+json
I0930 19:51:41.672929 1787965 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 19:51:41.672936 1787965 round_trippers.go:473]     Accept: application/json
I0930 19:51:41.677512 1787965 round_trippers.go:574] Response Status: 200 OK in 4 milliseconds
I0930 19:51:41.677535 1787965 round_trippers.go:577] Response Headers:
I0930 19:51:41.677543 1787965 round_trippers.go:580]     Date: Mon, 30 Sep 2024 19:51:41 GMT
I0930 19:51:41.677550 1787965 round_trippers.go:580]     Audit-Id: 153e9ab0-acff-4010-8b60-fd97c37c7ea2
I0930 19:51:41.677557 1787965 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 19:51:41.677563 1787965 round_trippers.go:580]     Content-Type: application/json
I0930 19:51:41.677569 1787965 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 19:51:41.677576 1787965 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 19:51:41.677582 1787965 round_trippers.go:580]     Content-Length: 2046
I0930 19:51:41.677618 1787965 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5807ba64-97ff-4eb9-a044-a1ca9a361351","resourceVersion":"6654","generation":3,"creationTimestamp":"2024-09-30T19:31:32Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T19:31:32Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"kubectl-patch","ope [truncated 1022 chars]
deployment.apps/nginx-0930 patched
```

Check the managedFields. The object has three owners, `kubectl-create`, `kubectl-patch`, and `kubectl-patch-again`.
```console
kubectl get deploy nginx-0930 -oyaml --show-managed-fields | yq .metadata.managedFields
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:metadata:
      f:labels:
        .: {}
        f:app: {}
    f:spec:
      f:progressDeadlineSeconds: {}
      f:revisionHistoryLimit: {}
      f:selector: {}
      f:strategy:
        f:rollingUpdate:
          .: {}
          f:maxSurge: {}
          f:maxUnavailable: {}
        f:type: {}
      f:template:
        f:metadata:
          f:labels:
            .: {}
            f:app: {}
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              .: {}
              f:imagePullPolicy: {}
              f:name: {}
              f:resources: {}
              f:terminationMessagePath: {}
              f:terminationMessagePolicy: {}
          f:dnsPolicy: {}
          f:restartPolicy: {}
          f:schedulerName: {}
          f:securityContext: {}
          f:terminationGracePeriodSeconds: {}
  manager: kubectl-create
  operation: Update
  time: "2024-09-30T19:31:32Z"
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:spec:
      f:template:
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              f:image: {}
  manager: kubectl-patch
  operation: Update
  time: "2024-09-30T19:42:47Z"
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:spec:
      f:replicas: {}
  manager: kubectl-patch-again
  operation: Update
  time: "2024-09-30T19:51:41Z"
```
We can see the manager `kubectl-patch-again` owns the 'replicas' field, but doesn't own the 'image' field.

Delete the object.
```console
kubectl delete -f nginx-0930.yaml
deployment.apps "nginx-0930" deleted
```