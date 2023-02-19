# Week 1 — App Containerization
## Livestream Technical Tasks
In this class, we are going to:
- [x] Create a new GitHub repo
- [x] Launch the repo within a Gitpod workspace
- [ ] Configure Gitpod.yml configuration, eg. VSCode Extensions
- [ ] Clone the frontend and backend repo
- [ ] Explore the codebases
- [ ] Ensure we can get the apps running locally
- [ ] Write a Dockerfile for each app
- [ ] Ensure we get the apps running via individual container
- [ ] Create a docker-compose file
- [ ] Ensure we can orchestrate multiple containers to run side by side
- [ ] Mount directories so we can make changes while we code

## Required Homework
- [x] Watch <a href="https://www.youtube.com/watch?v=FKAScachFgk&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=25">Grading Homework Summaries</a>
- [x] Watch Week 1 - <a href="https://www.youtube.com/watch?v=zJnNe5Nv4tE&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=22">Live Stream</a>
- [ ] Watch Ashish's Week 1 - <a href="https://www.youtube.com/watch?v=OjZz4D0B-cA&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=24">Container Security</a>
- [ ] Watch Ashish's Week 1 - <a href="https://www.youtube.com/watch?v=b-idMgFFcpg&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=23">Containerize Application (Dockerfiles, Docker Compose)</a>
- [ ] Document the Notification Endpoint for the OpenAI Document
- [ ] Write a Flask Backend Endpoint for Notifications
- [ ] Write a React Page for Notifications
- [ ] Run DynamoDB Local Container & ensure it works
- [ ] Run Postgres Container & ensure it works

## Homework Challenges
- [ ] Run the dockerfile CMD as an external script
- [ ] Push and tag a image to DockerHub (they have a free tier)
- [ ] Use multi-stage building for a Dockerfile build
- [ ] Implement a healthcheck in the V3 Docker compose file
- [ ] Research best practices of Dockerfiles and attempt to implement it in your Dockerfile
- [ ] Learn how to install Docker on your localmachine and get the same containers running outside of Gitpod / Codespaces
- [ ] Launch an EC2 instance that has docker installed, and pull a container to demonstrate you can run your own docker processes. 


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
