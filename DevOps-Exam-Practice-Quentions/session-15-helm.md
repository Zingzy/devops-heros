# MCQs — session-15-helm

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is Helm?

A. A package manager for Kubernetes
B. A container runtime
C. A network protocol
D. A cloud hypervisor

### Q2. What is a Helm chart?

A. A persistent disk
B. A running Pod
C. A Git branch
D. A package of Kubernetes templates and metadata

### Q3. What is Chart.yaml used for?

A. Pod runtime logs
B. Ingress certificates
C. Chart metadata such as name and version
D. Terraform state

### Q4. What is values.yaml used for?

A. Default configurable values for templates
B. Git merge history
C. Container registry authentication only
D. Linux process IDs

### Q5. Which command creates a starter chart?

A. helm pod create
B. helm create
C. helm chart start
D. helm init cluster

### Q6. Which command installs a chart release?

A. helm install
B. helm push pod
C. helm apply
D. helm deploy node

### Q7. Which command updates an installed release?

A. helm restart node
B. helm rerun
C. helm upgrade
D. helm patch image

### Q8. Which command returns to an earlier release revision?

A. helm revert image
B. helm reset cluster
C. helm rollback
D. helm undo commit

### Q9. Which flag can override a value on the command line?

A. --copy
B. --set
C. --port-forward
D. --replace-node

### Q10. Which command renders templates without installing?

A. helm template
B. helm render-pod
C. helm build-image
D. helm dryrun-cluster

---

## Answer Key

1-A, 2-D, 3-C, 4-A, 5-B, 6-A, 7-C, 8-C, 9-B, 10-A

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a Helm chart for a simple web application. Explain the purpose of Chart.yaml, values.yaml, and the templates directory.

### Lab 2
Deploy the chart with configurable image, replica count, and Service port values. Verify the rendered and installed Kubernetes resources.

### Lab 3
Upgrade a Helm release, inspect its revision history, and roll back to the previous revision. Verify the final release status.

