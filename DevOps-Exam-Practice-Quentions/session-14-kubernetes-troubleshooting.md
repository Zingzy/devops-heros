# MCQs — session-14-kubernetes-troubleshooting

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. Which command gives a quick overview of Pod status?

A. kubectl get pods
B. kubectl publish
C. kubectl init
D. kubectl build pods

### Q2. Which command displays detailed Pod events and conditions?

A. kubectl top namespace
B. kubectl apply -k
C. kubectl delete pod
D. kubectl describe pod

### Q3. Which command reads a container's logs?

A. kubectl version
B. kubectl create
C. kubectl label
D. kubectl logs

### Q4. Which command runs a command inside a running container?

A. kubectl exec
B. kubectl config view
C. kubectl explain
D. kubectl diff

### Q5. What often causes ImagePullBackOff?

A. An oversized log file only
B. A healthy application
C. A missing readiness probe only
D. An image cannot be downloaded

### Q6. What often causes CrashLoopBackOff?

A. A stable Service IP
B. A container repeatedly exits or crashes
C. A successful rollout
D. A valid PVC

### Q7. What is a common reason for a Pod to remain Pending?

A. Successful readiness probe
B. Correct image tag
C. Healthy DNS
D. Insufficient schedulable resources

### Q8. Where can you see recent scheduling or pull errors?

A. Kubernetes Events
B. Git tags
C. Docker Hub stars
D. Helm templates only

### Q9. What should you check if a Service has no endpoints?

A. Only the Git commit message
B. Whether its selector matches ready Pods
C. Only the cluster timezone
D. Only Docker build cache

### Q10. What is the final step after fixing an incident?

A. Delete all logs
B. Disable probes
C. Verify the workload behaves correctly
D. Skip testing

---

## Answer Key

1-A, 2-D, 3-D, 4-A, 5-D, 6-B, 7-D, 8-A, 9-B, 10-C

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Deploy a workload with an invalid image. Diagnose ImagePullBackOff using kubectl get, describe, and events, then correct the image.

### Lab 2
Diagnose a CrashLoopBackOff workload using logs and describe. Identify the root cause, fix the configuration, and verify recovery.

### Lab 3
Create a Service with an incorrect selector. Use labels, selectors, endpoints, and Service configuration to identify and fix the issue.

