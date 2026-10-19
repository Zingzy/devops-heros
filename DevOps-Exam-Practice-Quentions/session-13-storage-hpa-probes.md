# MCQs — session-13-storage-hpa-probes

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is a PersistentVolumeClaim (PVC)?

A. A request for persistent storage
B. A network firewall
C. A container image
D. A Git tag

### Q2. What is a PersistentVolume (PV)?

A. An Ingress controller
B. A cluster storage resource
C. A Deployment revision
D. A DNS zone

### Q3. What does a StorageClass help define?

A. Which Git branch is default
B. Which HTTP path is matched
C. Which Dockerfile is used
D. How dynamic storage provisioning occurs

### Q4. What does HPA stand for?

A. HTTP Proxy Adapter
B. Helm Package Archive
C. Horizontal Pod Autoscaler
D. Host Port Allocator

### Q5. What does an HPA commonly adjust?

A. Container image contents
B. Number of Pod replicas
C. Git history
D. Node operating system

### Q6. What does a readiness probe determine?

A. Whether a container image exists
B. Whether a container should receive traffic
C. Whether Git is clean
D. Whether a node is a control plane

### Q7. What does a liveness probe help detect?

A. Whether a Service has a public IP
B. Whether a volume is encrypted
C. Whether Terraform is initialized
D. When a container should be restarted

### Q8. What does a startup probe help with?

A. Allowing slow-starting apps time to initialize
B. Provisioning a cloud account
C. Creating a Docker network
D. Checking Git credentials

### Q9. What can happen if a Pod's PVC remains unbound?

A. The image is rebuilt automatically
B. The Pod may remain Pending
C. The Pod is always Running
D. The Deployment is deleted

### Q10. Which command lists PVCs?

A. kubectl get hpa-only
B. kubectl get routes
C. kubectl get mounts
D. kubectl get pvc

---

## Answer Key

1-A, 2-B, 3-D, 4-C, 5-B, 6-B, 7-D, 8-A, 9-B, 10-D

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a PersistentVolumeClaim, mount it into a Pod, write a file, recreate the Pod, and verify that the file remains.

### Lab 2
Configure readiness and liveness probes for a sample application. Demonstrate how Kubernetes reacts when the application is not ready or becomes unhealthy.

### Lab 3
Configure an HPA for a Deployment with CPU requests defined. Generate load and observe replica scaling; document any cluster prerequisites.
