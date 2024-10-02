Create a Deploymet object by `kubectl apply --server-side` using `nginx-0930.yaml`.
```console
kubectl apply --server-side --field-manager jun -f nginx-0930.yaml -v 8
I1002 17:07:58.555101 2639457 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 17:07:58.555753 2639457 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 17:07:58.555767 2639457 round_trippers.go:469] Request Headers:
I1002 17:07:58.555777 2639457 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:07:58.555784 2639457 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:07:58.569634 2639457 round_trippers.go:574] Response Status: 200 OK in 13 milliseconds
I1002 17:07:58.569660 2639457 round_trippers.go:577] Response Headers:
I1002 17:07:58.569668 2639457 round_trippers.go:580]     Audit-Id: d3f52ca2-df9d-4662-abe5-ba934d4afad3
I1002 17:07:58.569676 2639457 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 17:07:58.569683 2639457 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 17:07:58.569691 2639457 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 17:07:58.569697 2639457 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:07:58 GMT
I1002 17:07:58.569703 2639457 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:07:58.569710 2639457 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:07:58.569716 2639457 round_trippers.go:580]     Accept-Ranges: bytes
I1002 17:07:58.569723 2639457 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:07:58.569729 2639457 round_trippers.go:580]     X-From-Cache: 1
I1002 17:07:58.569746 2639457 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:07:58.569811 2639457 round_trippers.go:580]     Vary: Accept-Encoding
I1002 17:07:58.569819 2639457 round_trippers.go:580]     Vary: Accept
I1002 17:07:58.597622 2639457 request.go:1169] Response Body:
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
I1002 17:07:58.618203 2639457 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:mainline","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 17:07:58.618267 2639457 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=jun&fieldValidation=Strict&force=false
I1002 17:07:58.618276 2639457 round_trippers.go:469] Request Headers:
I1002 17:07:58.618285 2639457 round_trippers.go:473]     Accept: application/json
I1002 17:07:58.618293 2639457 round_trippers.go:473]     Content-Type: application/apply-patch+yaml
I1002 17:07:58.618300 2639457 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:07:58.625189 2639457 round_trippers.go:574] Response Status: 201 Created in 6 milliseconds
I1002 17:07:58.625214 2639457 round_trippers.go:577] Response Headers:
I1002 17:07:58.625225 2639457 round_trippers.go:580]     Content-Type: application/json
I1002 17:07:58.625237 2639457 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:07:58.625244 2639457 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:07:58.625251 2639457 round_trippers.go:580]     Content-Length: 1665
I1002 17:07:58.625257 2639457 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:07:58 GMT
I1002 17:07:58.625264 2639457 round_trippers.go:580]     Audit-Id: 96d46148-a340-4a03-a26a-4c4fe65823cd
I1002 17:07:58.625270 2639457 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:07:58.625304 2639457 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5cc3d080-3bb4-4443-ad07-a9c007e06055","resourceVersion":"21851","generation":1,"creationTimestamp":"2024-10-02T17:07:58Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun","operation":"Apply","apiVersion":"apps/v1","time":"2024-10-02T17:07:58Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]},"spec": [truncated 641 chars]
deployment.apps/nginx-0930 serverside-applied
I1002 17:07:58.625590 2639457 apply.go:476] Running apply post-processor function
```
We can see an HTTP PATCH is sent to the apiserver.

Check the managedFields.
```console
kubectl get deploy nginx-0930 -oyaml --show-managed-fields | yq .metadata.managedFields
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:metadata:
      f:labels:
        f:app: {}
    f:spec:
      f:progressDeadlineSeconds: {}
      f:replicas: {}
      f:revisionHistoryLimit: {}
      f:selector: {}
      f:strategy:
        f:rollingUpdate:
          f:maxSurge: {}
          f:maxUnavailable: {}
        f:type: {}
      f:template:
        f:metadata:
          f:creationTimestamp: {}
          f:labels:
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
  manager: jun
  operation: Apply
  time: "2024-10-02T17:07:58Z"
```
The fields have a single manager which is `jun`.

The only difference between `nginx-0930.yaml` and `nginx-0930-stable.yaml` is the image tag.
We are going to use `nginx-0930-stable.yaml` in the next step.
```console
diff nginx-0930.yaml nginx-0930-stable.yaml
27c27
<       - image: nginx:mainline
---
>       - image: nginx:stable
```

`kubectl replace` the object using `nginx-0930-stable.yaml`, to change the image tag from `mainline` to `stable`.
```console
kubectl replace deploy nginx-0930 -f nginx-0930-stable.yaml -v 8
I1002 17:13:52.422532 2644455 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 17:13:52.423246 2644455 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 17:13:52.423260 2644455 round_trippers.go:469] Request Headers:
I1002 17:13:52.423269 2644455 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:13:52.423277 2644455 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:13:52.437662 2644455 round_trippers.go:574] Response Status: 200 OK in 14 milliseconds
I1002 17:13:52.437689 2644455 round_trippers.go:577] Response Headers:
I1002 17:13:52.437698 2644455 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:13:52.437708 2644455 round_trippers.go:580]     Vary: Accept-Encoding
I1002 17:13:52.437716 2644455 round_trippers.go:580]     Vary: Accept
I1002 17:13:52.437724 2644455 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:13:52.437731 2644455 round_trippers.go:580]     Audit-Id: 50319ad2-8a7e-42b2-932f-51a89a546adc
I1002 17:13:52.437738 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:13:52.437744 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:13:52.437751 2644455 round_trippers.go:580]     X-From-Cache: 1
I1002 17:13:52.437758 2644455 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:13:52 GMT
I1002 17:13:52.437775 2644455 round_trippers.go:580]     Accept-Ranges: bytes
I1002 17:13:52.437782 2644455 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 17:13:52.437787 2644455 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 17:13:52.437794 2644455 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 17:13:52.467528 2644455 request.go:1169] Response Body:
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
I1002 17:13:52.488673 2644455 round_trippers.go:463] GET https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930
I1002 17:13:52.488701 2644455 round_trippers.go:469] Request Headers:
I1002 17:13:52.488711 2644455 round_trippers.go:473]     Accept: application/json
I1002 17:13:52.488720 2644455 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:13:52.490781 2644455 round_trippers.go:574] Response Status: 200 OK in 2 milliseconds
I1002 17:13:52.490808 2644455 round_trippers.go:577] Response Headers:
I1002 17:13:52.490818 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:13:52.490826 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:13:52.490833 2644455 round_trippers.go:580]     Content-Length: 1665
I1002 17:13:52.490839 2644455 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:13:52 GMT
I1002 17:13:52.490846 2644455 round_trippers.go:580]     Audit-Id: d972016b-097b-42f2-a1be-5f7eb0c2a311
I1002 17:13:52.490852 2644455 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:13:52.490859 2644455 round_trippers.go:580]     Content-Type: application/json
I1002 17:13:52.490891 2644455 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5cc3d080-3bb4-4443-ad07-a9c007e06055","resourceVersion":"21851","generation":1,"creationTimestamp":"2024-10-02T17:07:58Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun","operation":"Apply","apiVersion":"apps/v1","time":"2024-10-02T17:07:58Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]},"spec": [truncated 641 chars]
I1002 17:13:52.491057 2644455 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default","resourceVersion":"21851"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:stable","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 17:13:52.491105 2644455 round_trippers.go:463] PUT https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=kubectl-replace&fieldValidation=Strict
I1002 17:13:52.491113 2644455 round_trippers.go:469] Request Headers:
I1002 17:13:52.491121 2644455 round_trippers.go:473]     Content-Type: application/json
I1002 17:13:52.491128 2644455 round_trippers.go:473]     Accept: application/json
I1002 17:13:52.491135 2644455 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:13:52.495789 2644455 round_trippers.go:574] Response Status: 200 OK in 4 milliseconds
I1002 17:13:52.495818 2644455 round_trippers.go:577] Response Headers:
I1002 17:13:52.495830 2644455 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:13:52.495839 2644455 round_trippers.go:580]     Content-Type: application/json
I1002 17:13:52.495846 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:13:52.495853 2644455 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:13:52.495861 2644455 round_trippers.go:580]     Content-Length: 1885
I1002 17:13:52.495867 2644455 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:13:52 GMT
I1002 17:13:52.495873 2644455 round_trippers.go:580]     Audit-Id: f0f68abe-3899-4e2f-8b8d-bf4255dda0dd
I1002 17:13:52.495906 2644455 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"5cc3d080-3bb4-4443-ad07-a9c007e06055","resourceVersion":"21923","generation":2,"creationTimestamp":"2024-10-02T17:07:58Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun","operation":"Apply","apiVersion":"apps/v1","time":"2024-10-02T17:07:58Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"kubectl-re [truncated 861 chars]
deployment.apps/nginx-0930 replaced
```
We can see an HTTP PUT is sent to apiserver.

Check the managedFields.
```console
kubectl get deploy nginx-0930 -oyaml --show-managed-fields | yq .metadata.managedFields
- apiVersion: apps/v1
  fieldsType: FieldsV1
  fieldsV1:
    f:metadata:
      f:labels:
        f:app: {}
    f:spec:
      f:progressDeadlineSeconds: {}
      f:replicas: {}
      f:revisionHistoryLimit: {}
      f:selector: {}
      f:strategy:
        f:rollingUpdate:
          f:maxSurge: {}
          f:maxUnavailable: {}
        f:type: {}
      f:template:
        f:metadata:
          f:creationTimestamp: {}
          f:labels:
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
  manager: jun
  operation: Apply
  time: "2024-10-02T17:07:58Z"
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
  time: "2024-10-02T17:13:52Z"
```
The fields have two managers, `jun` and `kubectl-replace`.
We can see the manager `kubectl-replace` exclusively owns the 'image' field (ownership taken from `jun`), but doesn't own any other fields.

Delete the object.
```console
kubectl delete -f nginx-0930.yaml
deployment.apps "nginx-0930" deleted
```

This experiment can also be done in a slightly different way in the first step.
In the first step, we do `kubectl create` to create the Deploymet object, instead of `kubectl apply --server-side`.
```console
kubectl create -f nginx-0930.yaml -v 8
I1002 17:19:44.521165 2649278 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 17:19:44.521803 2649278 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 17:19:44.521816 2649278 round_trippers.go:469] Request Headers:
I1002 17:19:44.521825 2649278 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:19:44.521833 2649278 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:19:44.536193 2649278 round_trippers.go:574] Response Status: 200 OK in 14 milliseconds
I1002 17:19:44.536218 2649278 round_trippers.go:577] Response Headers:
I1002 17:19:44.536227 2649278 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:19:44.536236 2649278 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:19:44.536243 2649278 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:19:44.536250 2649278 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:19:44 GMT
I1002 17:19:44.536256 2649278 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 17:19:44.536266 2649278 round_trippers.go:580]     Audit-Id: 4a954229-80bd-47c1-a2b4-0ce4f4ea41d3
I1002 17:19:44.536273 2649278 round_trippers.go:580]     Vary: Accept-Encoding
I1002 17:19:44.536279 2649278 round_trippers.go:580]     Vary: Accept
I1002 17:19:44.536285 2649278 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 17:19:44.536292 2649278 round_trippers.go:580]     X-From-Cache: 1
I1002 17:19:44.536298 2649278 round_trippers.go:580]     Accept-Ranges: bytes
I1002 17:19:44.536305 2649278 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 17:19:44.536311 2649278 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:19:44.564695 2649278 request.go:1169] Response Body:
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
I1002 17:19:44.584867 2649278 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:mainline","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 17:19:44.584935 2649278 round_trippers.go:463] POST https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments?fieldManager=kubectl-create&fieldValidation=Strict
I1002 17:19:44.584945 2649278 round_trippers.go:469] Request Headers:
I1002 17:19:44.584954 2649278 round_trippers.go:473]     Accept: application/json
I1002 17:19:44.584962 2649278 round_trippers.go:473]     Content-Type: application/json
I1002 17:19:44.584969 2649278 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:19:44.590508 2649278 round_trippers.go:574] Response Status: 201 Created in 5 milliseconds
I1002 17:19:44.590532 2649278 round_trippers.go:577] Response Headers:
I1002 17:19:44.590543 2649278 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:19:44.590551 2649278 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:19:44.590558 2649278 round_trippers.go:580]     Content-Length: 1673
I1002 17:19:44.590565 2649278 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:19:44 GMT
I1002 17:19:44.590571 2649278 round_trippers.go:580]     Audit-Id: a0e3e144-9f32-403b-b15d-4bc422306528
I1002 17:19:44.590578 2649278 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:19:44.590584 2649278 round_trippers.go:580]     Content-Type: application/json
I1002 17:19:44.590613 2649278 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"037dfd90-08c3-45e3-89ca-0492c3d74b6f","resourceVersion":"22001","generation":1,"creationTimestamp":"2024-10-02T17:19:44Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-10-02T17:19:44Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]} [truncated 649 chars]
deployment.apps/nginx-0930 created
```
We can see an HTTP POST is sent to the apiserver.

Check the managedFields.
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
  time: "2024-10-02T17:19:44Z"
```
The fields have a single manager which is `kubectl-create`.

`kubectl replace` the object using `nginx-0930-stable.yaml`, to change the image tag from `mainline` to `stable`.
```console
kubectl replace deploy nginx-0930 -f nginx-0930-stable.yaml -v 8
I1002 17:25:00.363179 2653526 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 17:25:00.363790 2653526 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 17:25:00.363805 2653526 round_trippers.go:469] Request Headers:
I1002 17:25:00.363814 2653526 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:25:00.363823 2653526 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:25:00.377742 2653526 round_trippers.go:574] Response Status: 200 OK in 13 milliseconds
I1002 17:25:00.377776 2653526 round_trippers.go:577] Response Headers:
I1002 17:25:00.377783 2653526 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 17:25:00.377788 2653526 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 17:25:00.377794 2653526 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:25:00.377802 2653526 round_trippers.go:580]     X-From-Cache: 1
I1002 17:25:00.377809 2653526 round_trippers.go:580]     Accept-Ranges: bytes
I1002 17:25:00.377816 2653526 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 17:25:00.377832 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:25:00.377838 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:25:00.377845 2653526 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 17:25:00.377851 2653526 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:25:00 GMT
I1002 17:25:00.377858 2653526 round_trippers.go:580]     Audit-Id: f3449e88-e244-4445-8a88-84347e39c801
I1002 17:25:00.377864 2653526 round_trippers.go:580]     Vary: Accept-Encoding
I1002 17:25:00.377870 2653526 round_trippers.go:580]     Vary: Accept
I1002 17:25:00.406433 2653526 request.go:1169] Response Body:
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
I1002 17:25:00.429542 2653526 round_trippers.go:463] GET https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930
I1002 17:25:00.429570 2653526 round_trippers.go:469] Request Headers:
I1002 17:25:00.429583 2653526 round_trippers.go:473]     Accept: application/json
I1002 17:25:00.429592 2653526 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:25:00.431642 2653526 round_trippers.go:574] Response Status: 200 OK in 2 milliseconds
I1002 17:25:00.431664 2653526 round_trippers.go:577] Response Headers:
I1002 17:25:00.431675 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:25:00.431684 2653526 round_trippers.go:580]     Content-Length: 1673
I1002 17:25:00.431692 2653526 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:25:00 GMT
I1002 17:25:00.431699 2653526 round_trippers.go:580]     Audit-Id: e4467d2d-63ac-41fa-878e-c0d496284044
I1002 17:25:00.431705 2653526 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:25:00.431711 2653526 round_trippers.go:580]     Content-Type: application/json
I1002 17:25:00.431718 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:25:00.431762 2653526 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"037dfd90-08c3-45e3-89ca-0492c3d74b6f","resourceVersion":"22001","generation":1,"creationTimestamp":"2024-10-02T17:19:44Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-10-02T17:19:44Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]} [truncated 649 chars]
I1002 17:25:00.431916 2653526 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default","resourceVersion":"22001"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:stable","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 17:25:00.431963 2653526 round_trippers.go:463] PUT https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=kubectl-replace&fieldValidation=Strict
I1002 17:25:00.431971 2653526 round_trippers.go:469] Request Headers:
I1002 17:25:00.431984 2653526 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 17:25:00.431992 2653526 round_trippers.go:473]     Accept: application/json
I1002 17:25:00.431998 2653526 round_trippers.go:473]     Content-Type: application/json
I1002 17:25:00.438285 2653526 round_trippers.go:574] Response Status: 200 OK in 6 milliseconds
I1002 17:25:00.438310 2653526 round_trippers.go:577] Response Headers:
I1002 17:25:00.438323 2653526 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 17:25:00.438334 2653526 round_trippers.go:580]     Content-Type: application/json
I1002 17:25:00.438341 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 17:25:00.438348 2653526 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 17:25:00.438355 2653526 round_trippers.go:580]     Content-Length: 1893
I1002 17:25:00.438361 2653526 round_trippers.go:580]     Date: Wed, 02 Oct 2024 17:25:00 GMT
I1002 17:25:00.438368 2653526 round_trippers.go:580]     Audit-Id: 2da6d4b5-deb7-4d75-8fc2-d3e171671807
I1002 17:25:00.438404 2653526 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"037dfd90-08c3-45e3-89ca-0492c3d74b6f","resourceVersion":"22065","generation":2,"creationTimestamp":"2024-10-02T17:19:44Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"kubectl-create","operation":"Update","apiVersion":"apps/v1","time":"2024-10-02T17:19:44Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{".":{},"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:labels":{".":{},"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"ku [truncated 869 chars]
deployment.apps/nginx-0930 replaced
```
We can see an HTTP PUT is sent to apiserver.

Check the managedFields.
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
  time: "2024-10-02T17:19:44Z"
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
  time: "2024-10-02T17:25:00Z"
```
The fields have two managers, `kubectl-create` and `kubectl-replace`.
We can see the manager `kubectl-replace` exclusively owns the 'image' field (ownership taken from `kubecctl-create`), but doesn't own any other fields.

Delete the object.
```console
kubectl delete -f nginx-0930.yaml
deployment.apps "nginx-0930" deleted
```
