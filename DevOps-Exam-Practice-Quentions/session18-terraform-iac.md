# MCQs — session18-terraform-iac

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is Terraform used for?

A. Writing application unit tests
B. Serving static HTML only
C. Monitoring CPU usage only
D. Provisioning and managing infrastructure as code

### Q2. Which command initializes providers and backend?

A. terraform output
B. terraform destroy
C. terraform apply
D. terraform init

### Q3. Which command previews infrastructure changes?

A. terraform show-only
B. terraform plan
C. terraform state rm
D. terraform fmt

### Q4. Which command applies the planned changes?

A. terraform fmt
B. terraform validate
C. terraform apply
D. terraform graph

### Q5. What does Terraform state track?

A. Only shell command history
B. Only application logs
C. Mappings between configuration and managed resources
D. Only Docker images

### Q6. What is a Terraform provider?

A. A Kubernetes Pod
B. Plugin for interacting with an API or platform
C. A Linux package manager
D. A Git commit

### Q7. What is a Terraform module?

A. Reusable group of Terraform configuration
B. A DNS record type
C. A container image
D. An HTTP load balancer

### Q8. Which command checks Terraform configuration syntax and consistency?

A. terraform destroy
B. terraform output
C. terraform import
D. terraform validate

### Q9. What is a variable in Terraform?

A. An automatically encrypted password
B. An input used to parameterize configuration
C. A Helm release
D. A running cloud VM

### Q10. Why use a remote backend with locking?

A. Share state safely and reduce concurrent update conflicts
B. Run Pods without nodes
C. Replace all version control
D. Eliminate the need for credentials

---

## Answer Key

1-D, 2-D, 3-B, 4-C, 5-C, 6-B, 7-A, 8-D, 9-B, 10-A

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Write Terraform configuration that declares a provider and creates a small supported resource. Run fmt, init, validate, and plan, then explain the output.

### Lab 2
Use variables and outputs in a Terraform configuration. Pass a variable through a .tfvars file and print a useful output after apply.

### Lab 3
Modify a resource configuration, inspect the plan before applying, and explain how Terraform state maps configuration to real infrastructure. Do not commit secrets or state files.

 
