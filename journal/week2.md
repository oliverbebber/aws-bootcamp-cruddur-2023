# Week 2 — Distributed Tracing

## Required Homework
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 
- [ ] 

## Homework Challenges
- [ ] Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend[HARD]
- [ ] Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span
- [ ] Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces

# What is Distributed Tracing?
Distributed tracing is a technique used in software development to help identify and debug problems that occur in complex, distributed systems. In a distributed system, different components of an application can run on different servers, in different programming languages, and may communicate with each other using various communication protocols. It involves instrumenting an application to generate trace data, which provides a detailed view of how requests flow through the different components of a system. 

A trace represents a single request and includes information about the components that were involved in processing the request, the time taken by each component, and any errors that occurred along the way. Tools can be used to collect and visualize trace data, making it easier to understand the performance and behavior of a system as a whole. This can help identify bottlenecks, errors, and other issues that might be impacting the overall performance of the application. 


<img src="./assets/week2/slow-api-trace-sidebar.png">

## What is Instrumenting?
Instrumenting refers to the process of adding code to an application to collect data about its behavior, performance, or usage. The goal of instrumenting an application is to gain insight into how the application is functioning, to identify and fix issues, optimize performance, and improve user experience.

# Homework Challenges
## Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend[HARD]

## Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span

## Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces