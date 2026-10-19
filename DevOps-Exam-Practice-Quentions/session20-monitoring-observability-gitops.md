# MCQs — session20-monitoring-observability-gitops

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is a metric?

A. A YAML parser
B. A complete container image
C. A Git branch
D. A numeric measurement over time

### Q2. What is a log?

A. A cloud region
B. A persistent volume claim
C. A DNS subnet
D. A timestamped record of events

### Q3. What is a distributed trace?

A. A view of a request across services
B. A Docker image tag
C. A Git commit hash only
D. A shell variable

### Q4. What is Prometheus commonly used for?

A. Building Docker images
B. Provisioning VPCs
C. Collecting and querying time-series metrics
D. Hosting Git repositories

### Q5. What is Grafana commonly used for?

A. Visualizing metrics and creating dashboards
B. Building Helm charts
C. Scanning source code
D. Scheduling Kubernetes Pods

### Q6. What does observability help engineers do?

A. Avoid all incident response
B. Infer internal system behavior from telemetry
C. Disable logs
D. Replace application testing

### Q7. What is GitOps?

A. Replacing Kubernetes with Git
B. Storing passwords in plaintext
C. Running all changes manually
D. Managing desired system state through version-controlled Git

### Q8. In GitOps, what is the source of truth?

A. An untracked server file
B. A developer's local terminal
C. A random running Pod
D. The desired configuration stored in Git

### Q9. What is Argo CD commonly used for?

A. Reconciling Kubernetes deployments with Git
B. Creating Docker base images
C. Resolving DNS on a laptop
D. Compiling Java source code

### Q10. What does configuration drift mean?

A. Actual state differs from declared desired state
B. All Pods have identical images
C. Every Git branch is merged
D. Metrics are stored in a database

---

## Answer Key

1-D, 2-D, 3-A, 4-C, 5-A, 6-B, 7-D, 8-D, 9-A, 10-A

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Expose application metrics and configure Prometheus to scrape them. Verify the target is healthy and identify at least two metrics.

### Lab 2
Create a Grafana dashboard with panels for request rate, errors, and latency, or use the metrics available in the supplied environment. Explain what each panel indicates.

### Lab 3
Configure a basic GitOps deployment using Argo CD or a supplied GitOps environment. Change the desired replica count in Git and verify reconciliation in the cluster.

 
