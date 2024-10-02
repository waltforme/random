Create a Deploymet object by `kubectl apply --server-side` using `nginx-0930.yaml`.
```console
kubectl apply --server-side --field-manager jun -f nginx-0930.yaml -v 8
I1001 21:53:28.471015 2259008 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/managedfields/mypki/admin.kubeconfig
I1001 21:53:28.471610 2259008 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1001 21:53:28.471623 2259008 round_trippers.go:469] Request Headers:
I1001 21:53:28.471633 2259008 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1001 21:53:28.471640 2259008 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1001 21:53:28.485795 2259008 round_trippers.go:574] Response Status: 200 OK in 14 milliseconds
I1001 21:53:28.485823 2259008 round_trippers.go:577] Response Headers:
I1001 21:53:28.485832 2259008 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1001 21:53:28.485840 2259008 round_trippers.go:580]     Date: Tue, 01 Oct 2024 21:53:28 GMT
I1001 21:53:28.485847 2259008 round_trippers.go:580]     Audit-Id: edaedbf0-c327-41be-bcba-43e0e484844d
I1001 21:53:28.485853 2259008 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1001 21:53:28.485872 2259008 round_trippers.go:580]     X-From-Cache: 1
I1001 21:53:28.485878 2259008 round_trippers.go:580]     Cache-Control: no-cache, private
I1001 21:53:28.485884 2259008 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1001 21:53:28.485891 2259008 round_trippers.go:580]     Accept-Ranges: bytes
I1001 21:53:28.485898 2259008 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1001 21:53:28.485905 2259008 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1001 21:53:28.485912 2259008 round_trippers.go:580]     Vary: Accept-Encoding
I1001 21:53:28.485918 2259008 round_trippers.go:580]     Vary: Accept
I1001 21:53:28.485924 2259008 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1001 21:53:28.514442 2259008 request.go:1169] Response Body:
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
I1001 21:53:28.535489 2259008 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:mainline","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1001 21:53:28.535552 2259008 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=jun&fieldValidation=Strict&force=false
I1001 21:53:28.535561 2259008 round_trippers.go:469] Request Headers:
I1001 21:53:28.535570 2259008 round_trippers.go:473]     Content-Type: application/apply-patch+yaml
I1001 21:53:28.535577 2259008 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1001 21:53:28.535585 2259008 round_trippers.go:473]     Accept: application/json
I1001 21:53:28.540619 2259008 round_trippers.go:574] Response Status: 201 Created in 5 milliseconds
I1001 21:53:28.540640 2259008 round_trippers.go:577] Response Headers:
I1001 21:53:28.540651 2259008 round_trippers.go:580]     Content-Length: 1664
I1001 21:53:28.540659 2259008 round_trippers.go:580]     Date: Tue, 01 Oct 2024 21:53:28 GMT
I1001 21:53:28.540666 2259008 round_trippers.go:580]     Audit-Id: 263ee837-5290-4341-aab3-6acbb3d0411e
I1001 21:53:28.540672 2259008 round_trippers.go:580]     Cache-Control: no-cache, private
I1001 21:53:28.540679 2259008 round_trippers.go:580]     Content-Type: application/json
I1001 21:53:28.540685 2259008 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1001 21:53:28.540691 2259008 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1001 21:53:28.540721 2259008 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"52b9bfe8-dbe3-4bff-8d5c-4d1d1b7fdfce","resourceVersion":"7903","generation":1,"creationTimestamp":"2024-10-01T21:53:28Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun","operation":"Apply","apiVersion":"apps/v1","time":"2024-10-01T21:53:28Z","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}}]},"spec":{ [truncated 640 chars]
deployment.apps/nginx-0930 serverside-applied
I1001 21:53:28.541015 2259008 apply.go:476] Running apply post-processor function
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
  time: "2024-10-01T21:53:28Z"
```
The fields have a single manager which is `jun` (operation: Apply).

`kubectl apply --server-side` using the same `nginx-0930.yaml`, but as a second manager `jun-apply-again`.
```console
kubectl apply --server-side --field-manager jun-apply-again -f nginx-0930.yaml -v 8
I1002 01:55:31.267908 2333767 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 01:55:31.268529 2333767 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 01:55:31.268541 2333767 round_trippers.go:469] Request Headers:
I1002 01:55:31.268551 2333767 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 01:55:31.268558 2333767 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 01:55:31.988962 2333767 round_trippers.go:574] Response Status: 200 OK in 720 milliseconds
I1002 01:55:31.988992 2333767 round_trippers.go:577] Response Headers:
I1002 01:55:31.989002 2333767 round_trippers.go:580]     Audit-Id: 5e78b82f-5f3a-4df5-b99b-8d1379c69c48
I1002 01:55:31.989011 2333767 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 01:55:31.989018 2333767 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 01:55:31.989028 2333767 round_trippers.go:580]     X-From-Cache: 1
I1002 01:55:31.989035 2333767 round_trippers.go:580]     Vary: Accept-Encoding
I1002 01:55:31.989041 2333767 round_trippers.go:580]     Vary: Accept
I1002 01:55:31.989048 2333767 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 01:55:31.989054 2333767 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 01:55:31.989060 2333767 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 01:55:31.989066 2333767 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 01:55:31.989073 2333767 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 01:55:31.989079 2333767 round_trippers.go:580]     Accept-Ranges: bytes
I1002 01:55:31.989086 2333767 round_trippers.go:580]     Date: Wed, 02 Oct 2024 01:55:31 GMT
I1002 01:55:32.017334 2333767 request.go:1169] Response Body:
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
I1002 01:55:32.037321 2333767 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:mainline","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 01:55:32.037386 2333767 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=jun-apply-again&fieldValidation=Strict&force=false
I1002 01:55:32.037395 2333767 round_trippers.go:469] Request Headers:
I1002 01:55:32.037403 2333767 round_trippers.go:473]     Accept: application/json
I1002 01:55:32.037411 2333767 round_trippers.go:473]     Content-Type: application/apply-patch+yaml
I1002 01:55:32.037418 2333767 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 01:55:32.043808 2333767 round_trippers.go:574] Response Status: 200 OK in 6 milliseconds
I1002 01:55:32.043828 2333767 round_trippers.go:577] Response Headers:
I1002 01:55:32.043838 2333767 round_trippers.go:580]     Content-Type: application/json
I1002 01:55:32.043846 2333767 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 01:55:32.043853 2333767 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 01:55:32.043859 2333767 round_trippers.go:580]     Content-Length: 2388
I1002 01:55:32.043866 2333767 round_trippers.go:580]     Date: Wed, 02 Oct 2024 01:55:32 GMT
I1002 01:55:32.043872 2333767 round_trippers.go:580]     Audit-Id: 488da563-816a-4d0d-8030-f36fe7fe47c9
I1002 01:55:32.043878 2333767 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 01:55:32.043921 2333767 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"52b9bfe8-dbe3-4bff-8d5c-4d1d1b7fdfce","resourceVersion":"10825","generation":1,"creationTimestamp":"2024-10-01T21:53:28Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun-apply-again","operation":"Apply","apiVersion":"apps/v1","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:image":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"jun","operation [truncated 1364 chars]
deployment.apps/nginx-0930 serverside-applied
I1002 01:55:32.044304 2333767 apply.go:476] Running apply post-processor function
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
  manager: jun-apply-again
  operation: Apply
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
  time: "2024-10-01T21:53:28Z"
```
The fields have two managers, `jun` (operation: Apply) and `jun-apply-again` (operation: Apply).
Comparing the two managers, we can tell their managed fields are identical --- all the fields of the object.
The second manager somehow doesn't show `time`. Is it a bug? Will dig into it later.

The only difference between `nginx-0930.yaml` and `nginx-0930-stable.yaml` is the image tag.
We are going to use `nginx-0930-stable.yaml` in the next step.
```console
diff nginx-0930.yaml nginx-0930-stable.yaml
27c27
<       - image: nginx:mainline
---
>       - image: nginx:stable
```

`kubectl apply --server-side` using `nginx-0930-stable.yaml`, as a 3rd manager `jun-apply-3rd`.
```console
kubectl apply --server-side --field-manager jun-apply-3rd -f nginx-0930-stable.yaml -v 8
I1002 02:14:22.616912 2349162 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 02:14:22.617536 2349162 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 02:14:22.617550 2349162 round_trippers.go:469] Request Headers:
I1002 02:14:22.617559 2349162 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 02:14:22.617567 2349162 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 02:14:22.631135 2349162 round_trippers.go:574] Response Status: 200 OK in 13 milliseconds
I1002 02:14:22.631161 2349162 round_trippers.go:577] Response Headers:
I1002 02:14:22.631170 2349162 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 02:14:22.631178 2349162 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 02:14:22.631185 2349162 round_trippers.go:580]     X-From-Cache: 1
I1002 02:14:22.631191 2349162 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 02:14:22.631198 2349162 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 02:14:22.631204 2349162 round_trippers.go:580]     Date: Wed, 02 Oct 2024 02:14:22 GMT
I1002 02:14:22.631210 2349162 round_trippers.go:580]     Vary: Accept-Encoding
I1002 02:14:22.631216 2349162 round_trippers.go:580]     Vary: Accept
I1002 02:14:22.631223 2349162 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 02:14:22.631229 2349162 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 02:14:22.631238 2349162 round_trippers.go:580]     Audit-Id: 0ca40a35-7d45-4260-a388-0a97dfccd00b
I1002 02:14:22.631244 2349162 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 02:14:22.631251 2349162 round_trippers.go:580]     Accept-Ranges: bytes
I1002 02:14:22.659693 2349162 request.go:1169] Response Body:
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
I1002 02:14:22.679720 2349162 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:stable","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 02:14:22.679781 2349162 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=jun-apply-3rd&fieldValidation=Strict&force=false
I1002 02:14:22.679791 2349162 round_trippers.go:469] Request Headers:
I1002 02:14:22.679805 2349162 round_trippers.go:473]     Accept: application/json
I1002 02:14:22.679812 2349162 round_trippers.go:473]     Content-Type: application/apply-patch+yaml
I1002 02:14:22.679819 2349162 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 02:14:22.684275 2349162 round_trippers.go:574] Response Status: 409 Conflict in 4 milliseconds
I1002 02:14:22.684306 2349162 round_trippers.go:577] Response Headers:
I1002 02:14:22.684316 2349162 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 02:14:22.684324 2349162 round_trippers.go:580]     Content-Length: 613
I1002 02:14:22.684334 2349162 round_trippers.go:580]     Date: Wed, 02 Oct 2024 02:14:22 GMT
I1002 02:14:22.684341 2349162 round_trippers.go:580]     Audit-Id: c608b641-e6ef-4178-afda-31c6afeb6d2c
I1002 02:14:22.684348 2349162 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 02:14:22.684353 2349162 round_trippers.go:580]     Content-Type: application/json
I1002 02:14:22.684361 2349162 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 02:14:22.684387 2349162 request.go:1171] Response Body: {"kind":"Status","apiVersion":"v1","metadata":{},"status":"Failure","message":"Apply failed with 2 conflicts: conflicts with \"jun\":\n- .spec.template.spec.containers[name=\"nginx\"].image\nconflicts with \"jun-apply-again\":\n- .spec.template.spec.containers[name=\"nginx\"].image","reason":"Conflict","details":{"causes":[{"reason":"FieldManagerConflict","message":"conflict with \"jun-apply-again\"","field":".spec.template.spec.containers[name=\"nginx\"].image"},{"reason":"FieldManagerConflict","message":"conflict with \"jun\"","field":".spec.template.spec.containers[name=\"nginx\"].image"}]},"code":409}
error: Apply failed with 2 conflicts: conflicts with "jun":
- .spec.template.spec.containers[name="nginx"].image
conflicts with "jun-apply-again":
- .spec.template.spec.containers[name="nginx"].image
Please review the fields above--they currently have other managers. Here
are the ways you can resolve this warning:
* If you intend to manage all of these fields, please re-run the apply
  command with the `--force-conflicts` flag.
* If you do not intend to manage all of the fields, please edit your
  manifest to remove references to the fields that should keep their
  current managers.
* You may co-own fields by updating your manifest to match the existing
  value; in this case, you'll become the manager if the other manager(s)
  stop managing the field (remove it from their configuration).
See https://kubernetes.io/docs/reference/using-api/server-side-apply/#conflicts
```
There are two conflicts, with the two previous managers respectively, on the 'image' field.
Note this line of the output: "You may co-own fields by updating your manifest to match the existing value". This co-ownership is consistent with what we observed right after applying as `jun-apply-again`.

Re-run the apply with the additional `--force-conflicts` flag.
```console
kubectl apply --server-side --field-manager jun-apply-3rd --force-conflicts -f nginx-0930-stable.yaml -v 8
I1002 02:45:59.141688 2371646 loader.go:373] Config loaded from file:  /home/ubuntu/debug/kubernetes/general/mypki/admin.kubeconfig
I1002 02:45:59.142389 2371646 round_trippers.go:463] GET https://127.0.0.1:6443/openapi/v2?timeout=32s
I1002 02:45:59.142401 2371646 round_trippers.go:469] Request Headers:
I1002 02:45:59.142409 2371646 round_trippers.go:473]     Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 02:45:59.142417 2371646 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 02:45:59.155862 2371646 round_trippers.go:574] Response Status: 200 OK in 13 milliseconds
I1002 02:45:59.155884 2371646 round_trippers.go:577] Response Headers:
I1002 02:45:59.155893 2371646 round_trippers.go:580]     X-Varied-Accept: application/com.github.proto-openapi.spec.v2@v1.0+protobuf
I1002 02:45:59.155900 2371646 round_trippers.go:580]     Audit-Id: ace4461a-897b-4bb4-9b5e-349db794ee50
I1002 02:45:59.155907 2371646 round_trippers.go:580]     Last-Modified: Mon, 30 Sep 2024 19:29:06 GMT
I1002 02:45:59.155913 2371646 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 02:45:59.155920 2371646 round_trippers.go:580]     Content-Type: application/com.github.proto-openapi.spec.v2.v1.0+protobuf
I1002 02:45:59.155926 2371646 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 02:45:59.155933 2371646 round_trippers.go:580]     Accept-Ranges: bytes
I1002 02:45:59.155940 2371646 round_trippers.go:580]     Etag: "260013D7B855AD1C459983A645A55950E77DF9C7F7B261A4E9EA9B0A63CAB9E0EFDBFD3B76EC9D393331A2224E26CD03F40C3A420639FD973CC796C648785F14"
I1002 02:45:59.155947 2371646 round_trippers.go:580]     X-From-Cache: 1
I1002 02:45:59.155953 2371646 round_trippers.go:580]     Vary: Accept-Encoding
I1002 02:45:59.155959 2371646 round_trippers.go:580]     Vary: Accept
I1002 02:45:59.155965 2371646 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 02:45:59.155971 2371646 round_trippers.go:580]     Date: Wed, 02 Oct 2024 02:45:59 GMT
I1002 02:45:59.184475 2371646 request.go:1169] Response Body:
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
I1002 02:45:59.205159 2371646 request.go:1171] Request Body: {"apiVersion":"apps/v1","kind":"Deployment","metadata":{"labels":{"app":"nginx-0930"},"name":"nginx-0930","namespace":"default"},"spec":{"progressDeadlineSeconds":600,"replicas":1,"revisionHistoryLimit":10,"selector":{"matchLabels":{"app":"nginx-0930"}},"strategy":{"rollingUpdate":{"maxSurge":"25%","maxUnavailable":"25%"},"type":"RollingUpdate"},"template":{"metadata":{"creationTimestamp":null,"labels":{"app":"nginx-0930"}},"spec":{"containers":[{"image":"nginx:stable","imagePullPolicy":"Always","name":"nginx","resources":{},"terminationMessagePath":"/dev/termination-log","terminationMessagePolicy":"File"}],"dnsPolicy":"ClusterFirst","restartPolicy":"Always","schedulerName":"default-scheduler","securityContext":{},"terminationGracePeriodSeconds":30}}},"status":{}}
I1002 02:45:59.205227 2371646 round_trippers.go:463] PATCH https://127.0.0.1:6443/apis/apps/v1/namespaces/default/deployments/nginx-0930?fieldManager=jun-apply-3rd&fieldValidation=Strict&force=true
I1002 02:45:59.205237 2371646 round_trippers.go:469] Request Headers:
I1002 02:45:59.205247 2371646 round_trippers.go:473]     Content-Type: application/apply-patch+yaml
I1002 02:45:59.205256 2371646 round_trippers.go:473]     Accept: application/json
I1002 02:45:59.205263 2371646 round_trippers.go:473]     User-Agent: kubectl/v1.26.1 (linux/arm64) kubernetes/8f94681
I1002 02:45:59.213477 2371646 round_trippers.go:574] Response Status: 200 OK in 8 milliseconds
I1002 02:45:59.213501 2371646 round_trippers.go:577] Response Headers:
I1002 02:45:59.213521 2371646 round_trippers.go:580]     Content-Length: 3111
I1002 02:45:59.213529 2371646 round_trippers.go:580]     Date: Wed, 02 Oct 2024 02:45:59 GMT
I1002 02:45:59.213536 2371646 round_trippers.go:580]     Audit-Id: 36a99b6b-0735-4825-bb0b-0d9c8d712d2f
I1002 02:45:59.213544 2371646 round_trippers.go:580]     Cache-Control: no-cache, private
I1002 02:45:59.213550 2371646 round_trippers.go:580]     Content-Type: application/json
I1002 02:45:59.213557 2371646 round_trippers.go:580]     X-Kubernetes-Pf-Flowschema-Uid: 2ad18a02-df94-44d4-96dd-03c2492a970f
I1002 02:45:59.213564 2371646 round_trippers.go:580]     X-Kubernetes-Pf-Prioritylevel-Uid: d6c51cd3-f789-4396-bbdc-e88cbc763635
I1002 02:45:59.213611 2371646 request.go:1171] Response Body: {"kind":"Deployment","apiVersion":"apps/v1","metadata":{"name":"nginx-0930","namespace":"default","uid":"52b9bfe8-dbe3-4bff-8d5c-4d1d1b7fdfce","resourceVersion":"11435","generation":2,"creationTimestamp":"2024-10-01T21:53:28Z","labels":{"app":"nginx-0930"},"managedFields":[{"manager":"jun-apply-again","operation":"Apply","apiVersion":"apps/v1","fieldsType":"FieldsV1","fieldsV1":{"f:metadata":{"f:labels":{"f:app":{}}},"f:spec":{"f:progressDeadlineSeconds":{},"f:replicas":{},"f:revisionHistoryLimit":{},"f:selector":{},"f:strategy":{"f:rollingUpdate":{"f:maxSurge":{},"f:maxUnavailable":{}},"f:type":{}},"f:template":{"f:metadata":{"f:creationTimestamp":{},"f:labels":{"f:app":{}}},"f:spec":{"f:containers":{"k:{\"name\":\"nginx\"}":{".":{},"f:imagePullPolicy":{},"f:name":{},"f:resources":{},"f:terminationMessagePath":{},"f:terminationMessagePolicy":{}}},"f:dnsPolicy":{},"f:restartPolicy":{},"f:schedulerName":{},"f:securityContext":{},"f:terminationGracePeriodSeconds":{}}}}}},{"manager":"jun","operation":"Apply","ap [truncated 2087 chars]
deployment.apps/nginx-0930 serverside-applied
I1002 02:45:59.214136 2371646 apply.go:476] Running apply post-processor function
```

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
  manager: jun-apply-again
  operation: Apply
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
  time: "2024-10-01T21:53:28Z"
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
  manager: jun-apply-3rd
  operation: Apply
  time: "2024-10-02T02:45:59Z"
```
The fields have three managers, `jun` (operation: Apply), `jun-apply-again` (operation: Apply), and `jun-apply-3rd` (operation: Apply).
`jun-apply-3rd` manages all the fields as promised. `jun` and `jun-apply-again` lose the ownership of the conflicting 'image' field.

Delete the object.
```console
kubectl delete -f nginx-0930.yaml
deployment.apps "nginx-0930" deleted
```
