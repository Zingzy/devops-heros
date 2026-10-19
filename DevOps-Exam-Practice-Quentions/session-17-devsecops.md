# MCQs — session-17-devsecops

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. What is DevSecOps?

A. Avoiding dependency updates
B. Replacing CI with manual reviews
C. Running security only after release
D. Integrating security throughout development and delivery

### Q2. What does SAST analyze?

A. Source code or binaries without executing the application
B. Only production traffic
C. Only DNS responses
D. Only Kubernetes events

### Q3. What does DAST test?

A. Only Git commit messages
B. Only Docker layers
C. A running application from the outside
D. Only static source code

### Q4. What does dependency scanning identify?

A. Known vulnerabilities in third-party packages
B. Unused shell aliases
C. Missing Git branches
D. Slow DNS queries

### Q5. What does container image scanning inspect?

A. Only Kubernetes Service names
B. Image packages and known vulnerabilities
C. Only developer laptops
D. Only branch protections

### Q6. What is the principle of least privilege?

A. Disable authentication
B. Grant only permissions required
C. Share one token everywhere
D. Grant administrator rights to all

### Q7. Why should secrets not be committed to Git?

A. They may be exposed through repository history
B. They break YAML parsing
C. Git cannot store text
D. They prevent all merges

### Q8. What is an SBOM?

A. Software Bill of Materials listing components
B. Secure Backup Operating Mode
C. Source Branch Ownership Matrix
D. Server Build Output Map

### Q9. What is a common purpose of a security gate in CI?

A. Disable audit logs
B. Block promotion when policy checks fail
C. Allow all vulnerabilities
D. Skip all unit tests

### Q10. What does shift-left security mean?

A. Run security checks earlier in development
B. Move production servers physically
C. Only scan after deployment
D. Remove review from pipelines

---

## Answer Key

1-D, 2-A, 3-C, 4-A, 5-B, 6-B, 7-A, 8-A, 9-B, 10-A

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a CI/CD pipeline that builds a Docker image and pushes it to a container registry using repository secrets rather than hard-coded credentials.

### Lab 2
Add SAST, dependency scanning, and secret scanning to a pipeline. Configure a required security check to block later stages when it fails.

### Lab 3
Add container image vulnerability scanning and implement a gate that prevents deployment when the agreed severity threshold is exceeded.
