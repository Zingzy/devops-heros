# Session 13: Kubernetes storage, HPA and probes

- Name: Aditya Singhi
- Enrollment number: 24BCS10177

Run on a single node kind cluster (Kubernetes v1.37.0). kind ships the
`local-path` provisioner as its default StorageClass, so dynamic provisioning
works without extra setup. The HPA needs metrics-server, which I installed from
the upstream release with `--kubelet-insecure-tls` added (see Notes).

## Task 1: Kubernetes volumes

The documentation, with commands and output from this cluster, is in
[`01-kubernetes-volumes/README.md`](01-kubernetes-volumes/README.md). It covers
`emptyDir`, `hostPath`, PersistentVolume, PersistentVolumeClaim, StorageClass and
dynamic provisioning.

![PVC pending until a pod consumes it](screenshots/01-dynamic-provisioning.png)

## Task 2: HPA hands-on

I used `hpa/hpa-backend.yaml`, `hpa/backend-service.yaml` and
`hpa/load_generator.sh` from the session folder. The HPA targets the
`yatri-backend` Deployment from session 12, so its ConfigMap, Secret and
Deployment come from there. My copy of the HPA is
[`task2-hpa/hpa-backend.yaml`](task2-hpa/hpa-backend.yaml), unchanged.

### 1. Deploy the application

```bash
P12=../session-12-ingress-configmaps-secrets/04-full-demo
kubectl apply -f $P12/configmap.yaml -f $P12/secret.yaml -f $P12/backend.yaml
kubectl apply -f hpa/backend-service.yaml
kubectl rollout status deployment/yatri-backend
```

```
configmap/yatri-app-config created
secret/yatri-db-secret created
deployment.apps/yatri-backend created
service/yatri-backend-service created
service/yatri-backend-service configured
deployment "yatri-backend" successfully rolled out
```

The backend requests `cpu: 50m`. The HPA measures utilization as a percentage of
that request, so 25m per pod is the 50 percent target.

### 2 and 3. Configure and verify the HPA

```bash
kubectl apply -f hpa/hpa-backend.yaml
kubectl get hpa
```

```
horizontalpodautoscaler.autoscaling/yatri-backend-hpa created
NAME                REFERENCE                  TARGETS              MINPODS   MAXPODS   REPLICAS   AGE
yatri-backend-hpa   Deployment/yatri-backend   cpu: <unknown>/50%   2         10        0          0s
```

`<unknown>` lasts until metrics-server has a first sample. 45 seconds later:

```
NAME                REFERENCE                  TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
yatri-backend-hpa   Deployment/yatri-backend   cpu: 8%/50%   2         10        2          47s
```

### 4. Deploy a load generator

`load_generator.sh` defaults to `http://localhost:5000`, and on macOS port 5000
belongs to the AirPlay receiver:

```bash
curl -s -o /dev/null -w "%{http_code} %{header_json}\n" http://localhost:5000/healthz
```

```
403 {"content-length":["0"],
"server":["AirTunes/940.23.1"],
...
```

So I gave the script a port-forward on another port:

```bash
kubectl port-forward svc/yatri-backend-service 18130:80 &
bash hpa/load_generator.sh http://localhost:18130/healthz
```

The HPA never moved. Sampling `kubectl get hpa` and `kubectl top pods` every 15
seconds showed only one pod getting load, and the port-forward log shows the
tunnel dying:

```
=== t+71s 02:55:31
yatri-backend-hpa   Deployment/yatri-backend   cpu: 20%/50%   2     10    2     2m11s
yatri-backend-6c58cb99c7-crth5   17m   11Mi   
yatri-backend-6c58cb99c7-j9wpp   2m    10Mi   
```

```
Forwarding from 127.0.0.1:18130 -> 5000
...
E1007 02:56:38.300091   52531 portforward.go:501] "Error creating forwarding stream" err="Timeout occurred" localPort=18130 remotePort=5000
...
error: lost connection to pod
```

`kubectl port-forward svc/...` tunnels to a single pod, so new replicas would get
nothing. It also cannot carry 10 parallel curl loops. Load for an HPA has to go
through the Service from inside the cluster, so I used the generator from
`04-hpa/readme1.md`
([`task2-hpa/load-generator.yaml`](task2-hpa/load-generator.yaml) is the same pod
as a file):

```bash
kubectl run load-generator --image=busybox:1.36 --restart=Never -- /bin/sh -c \
  "while true; do wget -q -O- http://yatri-backend-service/healthz > /dev/null; done"
```

### 5, 6 and 7. Increase load, observe CPU and pod scaling

```bash
kubectl get hpa -w
```

```
NAME                REFERENCE                  TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
yatri-backend-hpa   Deployment/yatri-backend   cpu: 4%/50%    2         10        2          7m9s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 6%/50%    2         10        2          7m28s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 29%/50%   2         10        2          7m43s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 39%/50%   2         10        2          8m
yatri-backend-hpa   Deployment/yatri-backend   cpu: 74%/50%   2         10        2          8m21s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 61%/50%   2         10        3          8m36s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 48%/50%   2         10        3          8m52s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 71%/50%   2         10        3          9m7s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 64%/50%   2         10        5          9m23s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 57%/50%   2         10        5          9m38s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 51%/50%   2         10        5          9m55s
yatri-backend-hpa   Deployment/yatri-backend   cpu: 47%/50%   2         10        5          10m
```

The replica counts follow `ceil(replicas * current / target)`: `ceil(2 * 74 / 50)`
is 3, then `ceil(3 * 71 / 50)` is 5. It jumped from 3 to 5 in one step.

### 8 and 9. Captured output at 5 replicas

```bash
kubectl get hpa
kubectl get pods -o wide -l app=yatri-backend
kubectl top pods
kubectl describe hpa yatri-backend-hpa
```

```
NAME                REFERENCE                  TARGETS        MINPODS   MAXPODS   REPLICAS   AGE
yatri-backend-hpa   Deployment/yatri-backend   cpu: 47%/50%   2         10        5          10m
```

```
NAME                             READY   STATUS    RESTARTS   AGE    IP            NODE                 NOMINATED NODE   READINESS GATES
yatri-backend-6c58cb99c7-4r6fj   1/1     Running   0          2m3s   10.244.0.30   hw13-control-plane   <none>           <none>
yatri-backend-6c58cb99c7-5fv2f   1/1     Running   0          78s    10.244.0.32   hw13-control-plane   <none>           <none>
yatri-backend-6c58cb99c7-crth5   1/1     Running   0          10m    10.244.0.27   hw13-control-plane   <none>           <none>
yatri-backend-6c58cb99c7-j9wpp   1/1     Running   0          10m    10.244.0.28   hw13-control-plane   <none>           <none>
yatri-backend-6c58cb99c7-t77lw   1/1     Running   0          78s    10.244.0.31   hw13-control-plane   <none>           <none>
```

```
NAME                             CPU(cores)   MEMORY(bytes)   
load-generator                   373m         1Mi             
yatri-backend-6c58cb99c7-4r6fj   21m          10Mi            
yatri-backend-6c58cb99c7-5fv2f   24m          10Mi            
yatri-backend-6c58cb99c7-crth5   25m          11Mi            
yatri-backend-6c58cb99c7-j9wpp   24m          10Mi            
yatri-backend-6c58cb99c7-t77lw   25m          11Mi            
```

```
Metrics:                                               ( current / target )
  resource cpu on pods  (as a percentage of request):  47% (23m) / 50%
Min replicas:                                          2
Max replicas:                                          10
Deployment pods:                                       5 current / 5 desired
...
Events:
  Type     Reason                        Age   From                       Message
  ----     ------                        ----  ----                       -------
...
  Normal   SuccessfulRescale             2m8s  horizontal-pod-autoscaler  New size: 3; reason: cpu resource utilization (percentage of request) above target
  Normal   SuccessfulRescale             81s   horizontal-pod-autoscaler  New size: 5; reason: cpu resource utilization (percentage of request) above target
```

The HPA settled at 23m per pod, just under target. The load generator itself
used 373m to make five backends use about 120m, so the client was the
bottleneck, not the app.

Once the load generator was deleted, the HPA went back to 2:

```
  Normal   SuccessfulRescale             39s                horizontal-pod-autoscaler  New size: 2; reason: All metrics below target
```

## Task 3: Mini project

All files from `mini-project/`, unedited: namespace, 500Mi RWO PVC, nginx
Deployment with startup, readiness and liveness probes, ClusterIP Service, and
an HPA from 2 to 5 replicas at 50 percent CPU.

### Deploy

```bash
kubectl apply -f mini-project/namespace.yaml -f mini-project/pvc.yaml
kubectl apply -f mini-project/deployment.yaml -f mini-project/service.yaml -f mini-project/hpa.yaml
kubectl get pods -n production-webapp -o wide
kubectl get pvc -n production-webapp
```

```
NAME                      READY   STATUS    RESTARTS   AGE   IP            NODE                 NOMINATED NODE   READINESS GATES
web-app-d45775485-brchm   1/1     Running   0          14s   10.244.0.35   hw13-control-plane   <none>           <none>
web-app-d45775485-mgq9q   1/1     Running   0          14s   10.244.0.36   hw13-control-plane   <none>           <none>
NAME       STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
web-data   Bound    pvc-9b3dcca6-9e07-424b-886c-33b9ab53fbef   500Mi      RWO            standard       <unset>                 14s
```

The PVC stayed `Pending` until the pods existed, because kind's class is
`WaitForFirstConsumer`. Both replicas share one RWO volume, which only works
because kind has a single node.

### Storage persistence

```bash
POD_NAME=$(kubectl get pods -n production-webapp -l app=web-app -o jsonpath='{.items[0].metadata.name}')
kubectl exec -n production-webapp "$POD_NAME" -- sh -c 'echo "Student: Aditya Singhi" > /data/student.txt'
kubectl delete pod -n production-webapp "$POD_NAME"
kubectl rollout status deploy/web-app -n production-webapp
NEW_POD=$(kubectl get pods -n production-webapp -l app=web-app --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}')
echo "new pod $NEW_POD:"
kubectl exec -n production-webapp "$NEW_POD" -- cat /data/student.txt
```

```
pod "web-app-d45775485-brchm" deleted from production-webapp namespace
...
new pod web-app-d45775485-xz9v8:
Student: Aditya Singhi
```

I read from the newest pod on purpose. The project's `.items[0]` can return the
surviving old replica, which would pass without testing a new pod.

### Service

```bash
kubectl port-forward -n production-webapp svc/web-service 18131:80 &
curl -s http://localhost:18131 | head -5
```

```
Forwarding from 127.0.0.1:18131 -> 80
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
...
```

### HPA scaling

```bash
kubectl run load-generator -n production-webapp --image=busybox:1.36 --restart=Never \
  -- /bin/sh -c "while true; do wget -q -O- http://web-service; done"
kubectl get hpa -n production-webapp -w
```

```
NAME          REFERENCE            TARGETS       MINPODS   MAXPODS   REPLICAS   AGE
web-app-hpa   Deployment/web-app   cpu: 1%/50%   2         5         2          83s
...
web-app-hpa   Deployment/web-app   cpu: 37%/50%   2         5         2          4m41s
...
web-app-hpa   Deployment/web-app   cpu: 34%/50%   2         5         2          5m42s
```

One generator never got past 37 percent. `kubectl top pods` showed why:

```bash
kubectl top pods -n production-webapp
```

```
NAME                      CPU(cores)   MEMORY(bytes)   
load-generator            485m         4Mi             
web-app-d45775485-mgq9q   29m          4Mi             
web-app-d45775485-xz9v8   26m          4Mi             
```

The `wget` loop burns far more CPU than nginx spends answering it. I started two
more generators (`load-generator-2` and `load-generator-3`, same command):

```
web-app-hpa   Deployment/web-app   cpu: 41%/50%   2         5         2          6m27s
web-app-hpa   Deployment/web-app   cpu: 68%/50%   2         5         2          6m42s
web-app-hpa   Deployment/web-app   cpu: 60%/50%   2         5         3          6m58s
```

It held at 3, since three clients could not push three nginx pods back over 50
percent. To see it reach the 5 replica maximum, I lowered the target to 30
percent with `kubectl patch`, and `ceil(3 * 42 / 30)` gave 5:

```
web-app-hpa   Deployment/web-app   cpu: 42%/30%   2         5         3          11m
web-app-hpa   Deployment/web-app   cpu: 19%/30%   2         5         5          11m
```

![Mini project HPA at 5 replicas](screenshots/02-hpa-scale-out.png)

After deleting the generators, it scaled back down once the 5 minute
stabilization window passed:

```
  Normal   SuccessfulRescale             5m55s  horizontal-pod-autoscaler  New size: 3; reason: All metrics below target
  Normal   SuccessfulRescale             5m40s  horizontal-pod-autoscaler  New size: 2; reason: All metrics below target
```

I then re-applied `mini-project/hpa.yaml` to restore the 50 percent target.

## Notes

- `02-persistent-storage/pvc.yaml` never binds to `student-pv`. With a default
  StorageClass, a PVC without `storageClassName` gets `standard` and is
  dynamically provisioned. Fixed with `storageClassName: ""` in
  [`pvc-static.yaml`](01-kubernetes-volumes/manifests/pvc-static.yaml).
- On kind, metrics-server needs `--kubelet-insecure-tls`. Without it, scraping
  fails with `x509: cannot validate certificate ... doesn't contain any IP SANs`.
- `hpa/load_generator.sh` cannot drive an HPA. Its default port 5000 is AirPlay
  on macOS, and `kubectl port-forward` sends everything to one pod.
- A single busybox `wget` loop is CPU bound before nginx is. It took three
  generators to scale the mini project.
