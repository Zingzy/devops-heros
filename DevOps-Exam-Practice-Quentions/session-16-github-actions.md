# MCQs — session-16-github-actions

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. Where are GitHub Actions workflow files normally stored?

A. .github/workflows/
B. .kube/actions/
C. .git/actions/
D. .docker/workflows/

### Q2. Which YAML key specifies workflow triggers?

A. jobs
B. env
C. on
D. steps

### Q3. What is a job in GitHub Actions?

A. A Docker volume
B. A Kubernetes Service
C. A group of steps run on a runner
D. A Git branch

### Q4. What does runs-on specify?

A. Runner environment for a job
B. Git default branch
C. Kubernetes namespace
D. Target Docker registry

### Q5. Which action commonly checks out repository code?

A. actions/checkout
B. actions/setup-dockerhub
C. github/create-branch
D. runner/load-repo

### Q6. What does a step's run field do?

A. Executes shell commands
B. Defines a Docker image digest
C. Schedules a Kubernetes node
D. Creates a cloud VPC automatically

### Q7. What does a step's uses field do?

A. Creates a new repository
B. Writes Terraform state
C. Invokes a reusable action
D. Starts an SSH daemon

### Q8. How should sensitive tokens be supplied to workflows?

A. GitHub Actions secrets
B. Committed to README
C. Hardcoded in YAML
D. Printed to logs

### Q9. What does needs do between jobs?

A. Set Git author
B. Select a Dockerfile stage
C. Define container port mapping
D. Declare job dependencies

### Q10. Which trigger runs a workflow on code pushes?

A. push
B. docker-build
C. commit-only
D. upload

---

## Answer Key

1-A, 2-C, 3-C, 4-A, 5-A, 6-A, 7-C, 8-A, 9-D, 10-A

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a GitHub Actions workflow triggered on push that checks out the repository, installs dependencies, and builds the application.

### Lab 2
Add an automated test step. Demonstrate that a failing test causes the workflow to fail and that a corrected test passes.

### Lab 3
Extend the workflow to upload a build artifact and make it downloadable from the Actions run.

