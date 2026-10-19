# MCQs — session-11-kubernetes-services

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. Why are Kubernetes Services used?

A. Provide stable access to a set of Pods
B. Compile application code
C. Build container images
D. Store Git history

### Q2. Which Service type is typically reachable only within the cluster?

A. ClusterIP
B. NodePort
C. LoadBalancer
D. ExternalName only

### Q3. Which Service type exposes a port on each node?

A. NodePort
B. ExternalName
C. Headless only
D. ClusterIP

### Q4. Which Service type commonly provisions an external load balancer on supported clouds?

A. LoadBalancer
B. ClusterIP
C. ExternalName
D. Headless

### Q5. How does a Service identify backend Pods?

A. Label selector
B. Node hostname only
C. Git branch name
D. Docker image digest

### Q6. What does a Service port targetPort refer to?

A. SSH port of the node
B. Port on a Git remote
C. Port on backend Pods
D. Port of the API server

### Q7. What is the role of kube-proxy in many clusters?

A. Build Dockerfiles
B. Schedule Pods
C. Store secrets in etcd
D. Implement Service traffic routing rules

### Q8. Which DNS name form can identify a Service across namespaces?

A. pod.image.registry.local
B. service.cluster.node.local
C. service.namespace.svc.cluster.local
D. namespace.service.github.io

### Q9. What does a headless Service commonly set?

A. replicas: 0
B. type: NodePort
C. hostNetwork: true
D. clusterIP: None

### Q10. Which command lists Services?

A. kubectl build svc
B. kubectl init service
C. kubectl get svc
D. kubectl get images

---

## Answer Key

1-A, 2-A, 3-A, 4-A, 5-A, 6-C, 7-D, 8-C, 9-D, 10-C

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Deploy an application with multiple replicas and create a ClusterIP Service that selects the correct Pods. Verify its endpoints.

### Lab 2
Create a NodePort Service and demonstrate access to the application through the exposed node port.

### Lab 3
Configure a Service whose port and targetPort differ. Verify that traffic reaches the intended container port.
