# MCQs — session10-k8s-core-objects

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is the purpose of a Deployment?

A. Store cluster state
B. Manage desired replicas and rolling updates
C. Expose a public DNS zone
D. Create container images

### Q2. What does a ReplicaSet ensure?

A. A desired number of matching Pods are running
B. Nodes never fail
C. Every Pod has a public IP
D. All images are signed

### Q3. Which field commonly sets Deployment replica count?

A. status.desiredNodes
B. spec.ports
C. metadata.replicas
D. spec.replicas

### Q4. What does a Pod label help with?

A. Allocating disk partitions
B. Installing Helm
C. Selecting and organizing resources
D. Encrypting image layers

### Q5. What is a label selector used for?

A. Selecting Git commits by date
B. Matching resources with specified labels
C. Choosing Docker build stages
D. Filtering shell history

### Q6. Which command scales a Deployment?

A. kubectl duplicate image
B. kubectl increase node
C. kubectl scale deployment
D. kubectl resize pod

### Q7. What happens when a Deployment Pod crashes?

A. A controller works to restore desired state
B. Git automatically rolls back
C. Kubernetes deletes the Deployment permanently
D. The cluster always stops

### Q8. Which command views rollout status?

A. kubectl get dns
B. kubectl rollout status deployment/name
C. kubectl helm status
D. kubectl logs nodes

### Q9. What does a rolling update do?

A. Gradually replace old Pods with new ones
B. Change namespace ownership
C. Restart the control plane
D. Delete all nodes first

### Q10. Which resource usually creates and manages ReplicaSets?

A. Secret
B. PersistentVolume
C. ConfigMap
D. Deployment

---

## Answer Key

1-B, 2-A, 3-D, 4-C, 5-B, 6-C, 7-A, 8-B, 9-A, 10-D

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a Pod running Nginx and inspect its status, labels, IP address, and logs using kubectl.

### Lab 2
Create a Deployment with two replicas, scale it to five, and then scale it back to two. Verify the replica count at each step.

### Lab 3
Deploy version 1 of an application, perform a rolling update to version 2, verify the rollout, and roll back to version 1.

 
