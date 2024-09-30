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
  time: "2024-09-30T20:19:33Z"
```

`kubectl replace` the object, to change the image tag from `mainline` to `stable`.
```console
kubectl replace deploy nginx-0930 -f nginx-0930-stable.yaml -v 8
I0930 20:24:30.031145 1798825 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/managedfields/mypki/admin.kubeconfig
I0930 20:24:30.031750 1798825 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I0930 20:24:30.031762 1798825 round_trippers.go:469] Request Headers:
I0930 20:24:30.031770 1798825 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I0930 20:24:30.031778 1798825 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 20:24:30.045089 1798825 round_trippers.go:574] Response Status: 200 OK in 13 milliseconds
I0930 20:24:30.045114 1798825 round_trippers.go:577] Response Headers:
I0930 20:24:30.045124 1798825 round_trippers.go:580]     Audit-Id: e630ed9b-0a96-4c67-8a99-b93e2600e089
I0930 20:24:30.045132 1798825 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 20:24:30.045139 1798825 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I0930 20:24:30.045152 1798825 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I0930 20:24:30.045159 1798825 round_trippers.go:580]     Vary: Accept-Encoding
I0930 20:24:30.045166 1798825 round_trippers.go:580]     Vary: Accept
I0930 20:24:30.045172 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 20:24:30.045178 1798825 round_trippers.go:580]     Date: Mon, 30 Sep 2024 20:24:30 GMT
I0930 20:24:30.045185 1798825 round_trippers.go:580]     Accept-Ranges: bytes
I0930 20:24:30.045191 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 20:24:30.045198 1798825 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I0930 20:24:30.045204 1798825 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I0930 20:24:30.045211 1798825 round_trippers.go:580]     X-From-Cache: 1
I0930 20:24:30.072944 1798825 request.go:1169] Response Body:
00000000  0a 03 32 2e 30 12 12 0a  0a 4b 75 62 65 72 6e 65  |..2.0....Kuberne|
00000010  74 65 73 12 04 31 2e 33  32 42 95 ba 35 12 8c 02  |tes..1.32B..5...|
00000020  0a 22 2f 2e 77 65 6c 6c  2d 6b 6e 6f 77 6e 2f 6f  |."/.well-known/o|
00000030  70 65 6e 69 64 2d 63 6f  6e 66 69 67 75 72 61 74  |penid-configurat|
00000040  69 6f 6e 2f 12 e5 01 12  e2 01 0a 09 57 65 6c 6c  |ion/........Well|
00000050  4b 6e 6f 77 6e 1a 57 67  65 74 20 73 65 72 76 69  |Known.Wget servi|
00000060  63 65 20 61 63 63 6f 75  6e 74 20 69 73 73 75 65  |ce account issue|
00000070  72 20 4f 70 65 6e 49 44  20 63 6f 6e 66 69 67 75  |r OpenID configu|
00000080  72 61 74 69 6f 6e 2c 20  61 6c 73 6f 20 6b 6e 6f  |ration, also kno|
00000090  77 6e 20 61 73 20 74 68  65 20 27 4f 49 44 43 20  |wn as the 'OIDC |
000000a0  64 69 73 63 6f 76 65 72  79 20 64 6f 63 27 2a 2a  |discovery doc'**|
000000b0  67 65 74 53 65 72 76 69  63 65 41 63 63 6f 75 6e  |getServiceAccoun|
000000c0  74 49 73 73 75 65 72 4f  70 65 6e 49 44 43 6f 6e  |tIssuerOpenIDCo [truncated 8171127 chars]
I0930 20:24:30.094527 1798825 round_trippers.go:463] GET https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930
I0930 20:24:30.094552 1798825 round_trippers.go:469] Request Headers:
I0930 20:24:30.094564 1798825 round_trippers.go:473]     Accept: application/json
I0930 20:24:30.094572 1798825 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 20:24:30.096625 1798825 round_trippers.go:574] Response Status: 200 OK in 2 milliseconds
I0930 20:24:30.096648 1798825 round_trippers.go:577] Response Headers:
I0930 20:24:30.096665 1798825 round_trippers.go:580]     Content-Type: application/json
I0930 20:24:30.096675 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 20:24:30.096682 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 20:24:30.096689 1798825 round_trippers.go:580]     Content-Length: 1672
I0930 20:24:30.096696 1798825 round_trippers.go:580]     Date: Mon, 30 Sep 2024 20:24:30 GMT
I0930 20:24:30.096702 1798825 round_trippers.go:580]     Audit-Id: 2445de5c-843f-4af3-a71a-11c650483d62
I0930 20:24:30.096708 1798825 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 20:24:30.096733 1798825 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"39b3a33a-e02f-4b58-a747-9437767b7fde","resourceVersion":"6993","generation":1,"creationTimestamp":"2024-09-30T20:19:33Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T20:19:33Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]}, [truncated 648 chars]
I0930 20:24:30.096887 1798825 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default","resourceVersion":"6993"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:stable","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I0930 20:24:30.096931 1798825 round_trippers.go:463] PUT https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=kubectl-replace&fieldValidation=Strict
I0930 20:24:30.096939 1798825 round_trippers.go:469] Request Headers:
I0930 20:24:30.096947 1798825 round_trippers.go:473]     Accept: application/json
I0930 20:24:30.096954 1798825 round_trippers.go:473]     Content-Type: application/json
I0930 20:24:30.096960 1798825 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I0930 20:24:30.102492 1798825 round_trippers.go:574] Response Status: 200 OK in 5 milliseconds
I0930 20:24:30.102522 1798825 round_trippers.go:577] Response Headers:
I0930 20:24:30.102531 1798825 round_trippers.go:580]     Audit-Id: 8ab1cd2b-781c-40b0-8833-e1582aa57f34
I0930 20:24:30.102538 1798825 round_trippers.go:580]     Cache-Control: no-cache, private
I0930 20:24:30.102545 1798825 round_trippers.go:580]     Content-Type: application/json
I0930 20:24:30.102551 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I0930 20:24:30.102557 1798825 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I0930 20:24:30.102564 1798825 round_trippers.go:580]     Content-Length: 1892
I0930 20:24:30.102570 1798825 round_trippers.go:580]     Date: Mon, 30 Sep 2024 20:24:30 GMT
I0930 20:24:30.102602 1798825 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"39b3a33a-e02f-4b58-a747-9437767b7fde","resourceVersion":"7054","generation":2,"creationTimestamp":"2024-09-30T20:19:33Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-09-30T20:19:33Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"kub [truncated 868 chars]
deployment.apps/nginx-0930 replaced
```
We can see an HTTP PUT is sent to apiserver.

Check the managedFields. The object has two owners, `kubectl-create` and `kubectl-replace`.
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
  time: "2024-09-30T20:19:33Z"
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:spec:
      f:template:
        f:spec:
          f:containers:
            k:{"name":"nginx"}:
              f:image: {}
  manager: kubectl-replace
  operation: Update
  time: "2024-09-30T20:24:30Z"
```
We can see the manager `kubectl-replace` owns the 'image' field, but doesn't own any other fields.

Delete the object.
```console
kubectl delete -f nginx-0930.yaml
deployment.apps "nginx-0930" deleted
```
