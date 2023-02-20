# Week 1 — App Containerization
## Livestream Technical Tasks
In this class, we are going to:
- [x] Create a new GitHub repo
- [x] Launch the repo within a Gitpod workspace
- [ ] Configure Gitpod.yml configuration, eg. VSCode Extensions
- [x] Clone the frontend and backend repo
- [x] Explore the codebases
- [x] Ensure we can get the apps running locally
- [x] Write a Dockerfile for each app
- [ ] Ensure we get the apps running via individual container
- [x] Create a docker-compose file
- [ ] Ensure we can orchestrate multiple containers to run side by side
- [ ] Mount directories so we can make changes while we code

## Required Homework
- [x] Watch <a href="https://www.youtube.com/watch?v=FKAScachFgk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=25">Grading Homework Summaries</a>
- [x] Watch Week 1 - <a href="https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=22">Live Stream</a>
- [x] <a href="https://www.youtube.com/watch?v=b-idMgFFcpg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23">Remember to Commit Your Code</a>
- [x] Watch Chirag's Week 1 - <a href="https://www.youtube.com/watch?v=OAMHu1NiYoI&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24">Spending Considerations</a>
- [x] Watch Ashish's Week 1 - <a href="https://www.youtube.com/watch?v=OjZz4D0B-cA&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24">Container Security</a>
- [ ] Watch Ashish's Week 1 - <a href="https://www.youtube.com/watch?v=b-idMgFFcpg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23">Containerize Application (Dockerfiles, Docker Compose)</a>
- [ ] <a href="https://www.youtube.com/watch?v=k-_o0cCpksk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=27">Document the Notification Endpoint for the OpenAI Document</a>
- [ ] <a href="https://www.youtube.com/watch?v=k-_o0cCpksk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=27">Write a Flask Backend Endpoint for Notifications</a>
- [ ] <a href="https://www.youtube.com/watch?v=k-_o0cCpksk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=27">Write a React Page for Notifications</a>
- [ ] <a href="https://www.youtube.com/watch?v=CbQNMaa6zTg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=28">Run DynamoDB Local Container & ensure it works</a>
- [ ] <a href="https://www.youtube.com/watch?v=CbQNMaa6zTg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=28">Run Postgres Container & ensure it works</a>

## Homework Challenges
- [ ] Run the dockerfile CMD as an external script
- [ ] Push and tag a image to DockerHub (they have a free tier)
- [ ] Use multi-stage building for a Dockerfile build
- [ ] Implement a healthcheck in the V3 Docker compose file
- [ ] Research best practices of Dockerfiles and attempt to implement it in your Dockerfile
- [ ] Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces
- [ ] Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 

<img src="./assets/week1/docker.png">


# Container Security
## What is Container Security?
The practice of protecting apps hosted on compute services like Containers. Common examples of apps can be Single Page Applications (SPAs), Microservices, APIs, etc.

- Container First Strategy
- Most apps are being developed with Containers & Cloud Native
- Reducing impact of breach - segregation of apps & related services
- Managed Container services means your security responsibility is focused on a few things (AWS ECS, AWS ECR next week)
- Automation can help reduce recovery times to a known good state quickly

## Why Container Security requires practice
- Complexity with Containers
- Relying on CSPs for features
- Unmanaged containers require more work than Managed containers
    - Managed containers are managed by the CSP

## Docker Architecture
Two main components
- Client
- Server

## Container Security Components
- Docker & Host Configuration
- Securing Images
- Secret Management
- Application Security
- Data Security
- Monitoring Containers
- Compliance Framework

## Security Best Practices
- Keep host & Docker updated with the latest security patches
- Docker daemon & containers should run in non-root user mode
- Image Vulnerability Scanning
    - Amazon Inspector
    - Clair requires a client and a server. It will download libraries to match if the image is vulnerable.
- Trusting a Private vs Public Image Registry
- No Sensitive Data in Dockerfiles or Images
- Use Secret Management Services to share secrets
    - AWS Secrets Manager can be used with some services, but not every service will integrate with it.
    - Hashicorp Vault is another option to use, there is a free and paid version. The free version requires managing the server and client yourself.
- Read-only file system & volume for Docker
- Separate databases for longterm storage
- Use DevSecOps practices while building application security
- Ensure all code is tested for vulnerabilities before releasing for production

Note: Container Escape is a security vulnerability that allows a bad actor to break out of a container and gain access to resources on the host operating system. This could compromise the security of the entire system. 

This vulnerability can be caused by a variety of factors:
- Kernel vulnerabilities
    - The host and the container share the same kernel, meaning kernel vulnerabilities may allow an attacker to break out of the container.
- Application vulnerabilities
    - If an app running inside the container has a vulnerability, this may be exploited to gain access to the host OS.
- Misconfigured container runtime
    - Misconfigurations can allow attackers to access additional resources.
- Privilege escalation
    - If a container has more permissions than required, such as running as the root user, an attacker might be able to use privilege escalation to gain access to the host OS. 

Container Escape can be avoided by following the security best practices mentioned above.

## Managed Container Services
Docker Compose and Docker containers work really well to build one app.
- The down side is that security patches and updates requires shutting down Docker, make the update, and restart the server. This can cause problems in enterprise environments.

AWS Managed Container Services can provide a better 

- AWS ECS
- AWS EKS
- AWS Fargate
- AWS App Runner
- AWS Copilot

# VSCode Docker Extension
Docker for VSCode makes it easy to work with Docker

https://code.visualstudio.com/docs/containers/overview

    Gitpod is preinstalled with theis extension