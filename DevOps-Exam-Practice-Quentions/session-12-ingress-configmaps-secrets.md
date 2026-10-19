# MCQs — session-12-ingress-configmaps-secrets

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What does Ingress commonly define?

A. HTTP/HTTPS routing rules to Services
B. Git branch protections
C. Node CPU architecture
D. Container build steps

### Q2. What is needed to implement Ingress rules?

A. A Git tag
B. A Terraform lock file
C. A Docker registry only
D. An Ingress controller

### Q3. What is a ConfigMap intended to store?

A. Persistent disk blocks
B. Passwords by default
C. Container images
D. Non-sensitive configuration data

### Q4. What is a Secret intended to store?

A. Sensitive configuration values
B. Container images
C. Cluster logs only
D. Helm binaries

### Q5. How can a ConfigMap be consumed by a Pod?

A. Node kernel flags only
B. Docker build cache only
C. Git commit messages only
D. Environment variables or mounted files

### Q6. What does a path rule in Ingress match?

A. Container filesystem path
B. The HTTP request path
C. Host disk mount path
D. Git remote path

### Q7. What does TLS termination usually provide at Ingress?

A. Automatic Pod autoscaling
B. Persistent volumes
C. Build artifact signing
D. HTTPS encryption for client connections

### Q8. Which command lists ConfigMaps?

A. kubectl get configmaps
B. kubectl get secrets-only
C. kubectl get networks
D. kubectl get charts

### Q9. Are Kubernetes Secret values encrypted merely because YAML uses base64?

A. Yes, base64 is strong encryption
B. No, base64 is encoding rather than encryption
C. Yes, they are always hashed
D. No, Secrets cannot contain strings

### Q10. Which Kubernetes resource commonly holds a TLS certificate and key for Ingress?

A. ConfigMap
B. Deployment
C. Secret
D. ServiceAccount only

---

## Answer Key

1-A, 2-D, 3-D, 4-A, 5-D, 6-B, 7-D, 8-A, 9-B, 10-C

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Deploy an application and configure an Ingress rule that routes requests by host or URL path to the correct Service.

### Lab 2
Create a ConfigMap and inject its values into a Deployment as environment variables. Verify the values inside a running Pod.

### Lab 3
Create a Kubernetes Secret for a sample credential and consume it from a Pod without hard-coding the credential in the Deployment manifest.

