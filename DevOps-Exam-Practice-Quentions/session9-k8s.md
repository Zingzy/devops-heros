# MCQs — session9-k8s

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is Kubernetes primarily used for?

A. Replacing Git history
B. Editing photos
C. Compiling Linux kernels
D. Orchestrating containerized applications

### Q2. What is a Kubernetes Pod?

A. A Terraform provider
B. A physical data center
C. Smallest deployable unit containing one or more containers
D. A Docker image registry

### Q3. Which component stores Kubernetes cluster state?

A. containerd
B. CoreDNS
C. etcd
D. kube-proxy

### Q4. Which component schedules Pods onto nodes?

A. kube-scheduler
B. kube-proxy
C. kubectl
D. kubelet

### Q5. What does the kubelet do?

A. Stores all cluster state
B. Builds Helm charts
C. Approves pull requests
D. Ensures Pod containers run on a node

### Q6. What is kubectl?

A. A Linux filesystem
B. A CLI for interacting with the Kubernetes API
C. A DNS protocol
D. A container image format

### Q7. Which command lists Pods?

A. kubectl show nodes
B. kubectl list images
C. kubectl build pods
D. kubectl get pods

### Q8. What is a Kubernetes namespace?

A. A Dockerfile instruction
B. A logical grouping for cluster resources
C. A container image tag
D. A dedicated physical server

### Q9. Which component exposes the Kubernetes API?

A. kubelet
B. kube-apiserver
C. CoreDNS
D. kube-proxy

### Q10. What is a worker node?

A. A DNS resolver record
B. A GitHub workflow file
C. A Helm repository
D. A machine that runs application Pods

---

## Answer Key

1-D, 2-C, 3-C, 4-A, 5-D, 6-B, 7-D, 8-B, 9-B, 10-D

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Connect to a Kubernetes cluster and inspect nodes, namespaces, and cluster resources using kubectl. Record what each command shows.

### Lab 2
Deploy a simple web application and inspect it using kubectl get, describe, and logs. Confirm that the workload reaches a healthy state.

### Lab 3
Identify the role of the API Server, Scheduler, Controller Manager, etcd, kubelet, and kubectl in a short cluster architecture diagram.

 
