# Task 1: Kubernetes volumes

- Name: Aditya Singhi
- Enrollment number: 24BCS10177

Run on the kind cluster from the main README, using the manifests in
`01-volumes/`, `02-persistent-storage/` and `03-storageclass/`. Where one did not
work as written, my fixed copy is in [`manifests/`](manifests/).

A container's own filesystem is lost when the container restarts. A volume is a
directory mounted from somewhere else, so data can outlive the container, or the
pod, depending on the volume type.

## emptyDir

An empty directory created with the pod and shared by its containers. It
survives container restarts but is deleted with the pod.

```bash
kubectl apply -f 01-volumes/emptydir-pod.yaml
kubectl exec emptydir-demo -- sh -c 'echo "Hello Kubernetes" > /data/message.txt; cat /data/message.txt'
kubectl delete pod emptydir-demo
kubectl apply -f 01-volumes/emptydir-pod.yaml
kubectl wait --for=condition=Ready pod/emptydir-demo
kubectl exec emptydir-demo -- cat /data/message.txt
```

```
...
Hello Kubernetes
...
pod "emptydir-demo" deleted from default namespace
pod/emptydir-demo created
pod/emptydir-demo condition met
cat: /data/message.txt: No such file or directory
command terminated with exit code 1
```

The recreated pod has a new UID, so it gets a new empty directory under
`/var/lib/kubelet/pods/<uid>/` on the node. Good for scratch space or sharing
files with a sidecar, not for data you need to keep.

## hostPath

Mounts a directory from the node into the pod.

```bash
kubectl apply -f 01-volumes/hostpath-pod.yaml
kubectl exec hostpath-demo -- sh -c 'echo "written from the pod" > /data/note.txt'
docker exec hw13-control-plane cat /tmp/hostpath-data/note.txt
kubectl delete pod hostpath-demo
kubectl apply -f 01-volumes/hostpath-pod.yaml
kubectl wait --for=condition=Ready pod/hostpath-demo
kubectl exec hostpath-demo -- cat /data/note.txt
```

```
...
written from the pod
pod "hostpath-demo" deleted from default namespace
pod/hostpath-demo created
pod/hostpath-demo condition met
written from the pod
```

The file lives on the kind node container, not on my Mac, and it survives the
pod. That only works because there is one node. On a real cluster the new pod
could land on another node with an empty directory, so `hostPath` suits node
level tools and labs, not application data.

## PersistentVolume and PersistentVolumeClaim

A PV is storage that exists in the cluster. A PVC is an application's request
for storage (size and access mode). The pod only names the claim.

Running the instructor manifests as written:

```bash
kubectl apply -f 02-persistent-storage/pv.yaml -f 02-persistent-storage/pvc.yaml
kubectl apply -f 02-persistent-storage/pod.yaml
kubectl get pvc
kubectl get pv
```

```
...
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
student-pvc   Bound    pvc-21a4d58a-ae19-456b-894f-326992bcbd42   500Mi      RWO            standard       <unset>                 7s
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS      CLAIM                 STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-21a4d58a-ae19-456b-894f-326992bcbd42   500Mi      RWO            Delete           Bound       default/student-pvc   standard       <unset>                          2s
student-pv                                 1Gi        RWO            Retain           Available                                        <unset>                          7s
```

The claim did not bind to `student-pv`. A PVC with no `storageClassName` gets
the default class (`standard`) written into it, and a claim only binds to a PV of
the same class. So the provisioner made a new volume and `student-pv` stayed
unused. [`manifests/pvc-static.yaml`](manifests/pvc-static.yaml) adds
`storageClassName: ""`, which means "no class":

```bash
kubectl delete pod storage-demo; kubectl delete pvc student-pvc
kubectl apply -f manifests/pvc-static.yaml
kubectl get pvc student-pvc
```

```
...
NAME          STATUS   VOLUME       CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
student-pvc   Bound    student-pv   1Gi        RWO                           <unset>                 3s
```

Bound to the 1Gi PV even though 500Mi was asked for. A PV goes to one claim,
whole. Persistence across pod deletion:

```bash
kubectl apply -f 02-persistent-storage/pod.yaml
kubectl exec storage-demo -- sh -c 'echo "Kubernetes Storage" > /data/message.txt'
kubectl delete pod storage-demo
kubectl apply -f 02-persistent-storage/pod.yaml
kubectl wait --for=condition=Ready pod/storage-demo
kubectl exec storage-demo -- cat /data/message.txt
```

```
...
pod "storage-demo" deleted from default namespace
pod/storage-demo created
pod/storage-demo condition met
Kubernetes Storage
```

`student-pv` uses `Retain`, so deleting the claim keeps the data and leaves the
PV `Released` until an admin clears its `claimRef`. Its access mode,
`ReadWriteOnce`, limits it to one node, not one pod.

## StorageClass and dynamic provisioning

A StorageClass names a provisioner that creates PVs on demand, so nobody has to
make them by hand.

```bash
kubectl get sc
kubectl apply -f 03-storageclass/pvc.yaml
kubectl get pvc dynamic-pvc
kubectl describe pvc dynamic-pvc | tail -1
```

```
NAME                 PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
standard (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  17s
persistentvolumeclaim/dynamic-pvc created
NAME          STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
dynamic-pvc   Pending                                      standard       <unset>                 5s
  Normal  WaitForFirstConsumer  5s (x2 over 5s)  persistentvolume-controller  waiting for first consumer to be created before binding
```

`Pending` is by design. `WaitForFirstConsumer` waits until a pod using the claim
is scheduled, then creates the volume on that pod's node. The notes have no pod
for this claim, so I wrote
[`manifests/dynamic-consumer-pod.yaml`](manifests/dynamic-consumer-pod.yaml):

```bash
kubectl apply -f manifests/dynamic-consumer-pod.yaml
kubectl wait --for=condition=Ready pod/dynamic-consumer
kubectl get pvc dynamic-pvc
kubectl get pv | grep -E "NAME|dynamic"
```

```
pod/dynamic-consumer created
pod/dynamic-consumer condition met
NAME          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
dynamic-pvc   Bound    pvc-89d29258-114a-44ec-b6d3-2bda121d51b4   500Mi      RWO            standard       <unset>                 17s
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                 STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-89d29258-114a-44ec-b6d3-2bda121d51b4   500Mi      RWO            Delete           Bound    default/dynamic-pvc   standard       <unset>                          2s
```

The provisioner created a PV of exactly 500Mi and the claim bound. The class has
`reclaimPolicy: Delete`, so deleting the claim later removed the PV and its data
too.

![PVC pending until a pod consumes it](../screenshots/01-dynamic-provisioning.png)

The screenshot is a second run of the same steps, so the volume name differs.
