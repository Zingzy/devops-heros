# MCQs — session8-docker-networking-volume

**10 multiple-choice questions | 1 mark each | Answer key at the end**

### Q1. Why use Docker volumes?

A. Increase CPU frequency
B. Disable networking
C. Persist data beyond a container lifecycle
D. Replace container images

### Q2. Which command lists Docker volumes?

A. docker volumes show
B. docker storage ps
C. docker volume ls
D. docker volume ps

### Q3. What is a bind mount?

A. A remote Git branch
B. A Kubernetes namespace
C. A host path mounted inside a container
D. An image registry

### Q4. Which Docker network driver is the typical default for standalone containers?

A. overlay
B. macvtap only
C. host-only VM
D. bridge

### Q5. What does a user-defined bridge network provide?

A. Host kernel upgrades
B. Container-to-container name resolution
C. Automatic cloud load balancing
D. Persistent image layers

### Q6. Which flag publishes a container port?

A.  -w 
B.  -e 
C.  -v 
D.  -p 

### Q7. Which command creates a Docker network?

A. docker net init
B. docker bridge build
C. docker network create
D. docker network push

### Q8. What is Docker Compose mainly for?

A. Replacing source control
B. Defining and running multi-container applications
C. Managing Linux users
D. Creating DNS root servers

### Q9. Which file is commonly used by Docker Compose?

A. Chart.yaml
B. terraform.tfstate
C. Jenkinsfile
D. compose.yaml

### Q10. Which command starts services from a Compose file?

A. docker compose attach-all
B. docker compose init-only
C. docker compose up
D. docker compose commit

---

## Answer Key

1-C, 2-C, 3-C, 4-D, 5-B, 6-D, 7-C, 8-B, 9-D, 10-C

---

## Practical / Lab Questions (Exam Style)

**Suggested format:** Complete the task in the relevant lab environment, submit commands/configuration files, and include brief evidence of verification. Do not hard-code credentials.

### Lab 1
Create a custom Docker network and run two containers on it. Demonstrate name-based communication between the containers.

### Lab 2
Run a database container with a named volume, create sample data, remove and recreate the container, and verify that the data persists.

### Lab 3
Write a compose.yaml file for a web application and database. Start the stack, verify service communication, inspect logs, and shut it down.

 
