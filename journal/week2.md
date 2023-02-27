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
- [x] Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces

# What is Distributed Tracing?
Distributed tracing is a technique used in software development to help identify and debug problems that occur in complex, distributed systems. In a distributed system, different components of an application can run on different servers, in different programming languages, and may communicate with each other using various communication protocols. It involves instrumenting an application to generate trace data, which provides a detailed view of how requests flow through the different components of a system. 

A trace represents a single request and includes information about the components that were involved in processing the request, the time taken by each component, and any errors that occurred along the way. Tools can be used to collect and visualize trace data, making it easier to understand the performance and behavior of a system as a whole. This can help identify bottlenecks, errors, and other issues that might be impacting the overall performance of the application. 


<img src="./assets/week2/slow-api-trace-sidebar.png">

## What is Instrumenting?
Instrumenting refers to the process of adding code to an application to collect data about its behavior, performance, or usage. The goal of instrumenting an application is to gain insight into how the application is functioning, to identify and fix issues, optimize performance, and improve user experience.

## What is observability?
<img src="./assets/week2/observability-three-pillars.jpg">

Observability is a concept in software engineering that refers to the ability to understand the internal state of a system based on its external behavior. Put simply, an observable system can be monitored, analyzed, and understood from the outside.

Observability is essential in modern software development because it allows developers and operators to gain insight into the behavior of complex, distributed systems. 

In a distributed system, different components of an application can run on different servers, in different programming languages, and may communicate with each other using various communication protocols. Observability tools allow developers and operators to track the flow of requests through the system, monitor system health and performance, and identify and troubleshoot issues as they arise.

- Metrics: collect valuable data regarding KPIs like error rates, latency, and throughput. 
- Traces: tracks each request as it occurs and analyzes the performance of each component that processes the requests.
- Logs: capture data from different components of a system and analyze the information to get insights into the an applications behavior.
- Dependencies: reveals how each component is dependent on other components, apps, and IT resources.

Source: https://www.ibm.com/topics/observability & https://newrelic.com/blog/best-practices/observability-instrumentation


# HoneyComb
## Create a HoneyComb account
https://www.honeycomb.io/

I had previously setup my HoneyComb account. If you need an account, go to the website about and click Get Started to begin creating your account.

## Set the API key & Service Name
```sh
export HONEYCOMB_API_KEY=""
export HONEYCOMB_SERVICE_NAME="Cruddur"
gp env HONEYCOMB_API_KEY=""
gp env HONEYCOMB_SERVICE_NAME="Cruddur"
````

<img src="./assets/week2/set-honeycomb-api-key.jpg">

<img src="./assets/week2/set-honeycomb-service-name.jpg">

NOTE: Instead of calling the HoneyComb Service Name "Cruddur", we will want to name it specifically the name of the service. 
- For example: we will rename this service name to "backend-flask"
- The overall project (Cruddur) should use the same API key, which will allow all services to work together, but each part of the project will have it's own service name.

<img src="./assets/week2/set-honeycomb-service-name-backend.jpg">

## Set Env Vars for ```backend-flask``` in ```docker-compose ```
Add the following to the backend-flask service.

```docker
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "backend-flask"
```

## Install Python Packages
```
cd backend-flask
pip install opentelemetry-api
```

Note: running ```pip install opentelemtry-api``` did NOT add to ```requirements.txt```

<img src="./assets/week2/python-package-requirements-file.jpg">

## Add Dependencies to ```requirements.txt```
```
opentelemetry-api
opentelemetry-sdk
opentelemetry-exporter-otlp-proto-http
opentelemetry-instrumentation-flask
opentelemetry-instrumentation-requests
```

Then run the following from the backend-flask directory

```py
pip install -r requirements.txt
```

## Add ```app.py``` Updates

```py
# HoneyComb Updates -------
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
```


```py
# HoneyComb Updates -------
# Initialize tracing and an exporter that can send data to Honeycomb
provider = TracerProvider()
processor = BatchSpanProcessor(OTLPSpanExporter())
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)
tracer = trace.get_tracer(__name__)
```

```py
# HoneyComb Updates -------
# Initialize automatic instrumentation with Flask
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
```

## Add Port Configuration to ```gitpod.yml```
```yml
ports:
  - name: frontend
    port: 3000
    onOpen: open-browser
    visibility: public
  - name: backend
    port: 4567
    visibility: public
  - name: xray-daemon
    port: 2000
    visibility: public
```

## Start Containers
```docker
docker compose up
```

## Add SimpleSpanProcessor (ConsoleSpanExporter) to ```app.py```
Under the first section for HoneyComb Updates:
```py
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
```

Add this to the second section of HoneyComb Updates (Initialize tracing & an exporter that can send data to Honeycomb)
```py
# Show this in logs within backend-flask app (STDOUT)
simple_processor = SimpleSpanProcessor(ConsoleSpanExporter())
provider.add_simple_span_processor(simple_processor)
```

### Check HoneyComb for Data
Click on Home & Spans should be displayed

<img src="./assets/week2/honeycomb-http-status-code.jpg">

<img src="./assets/week2/single-span-trace.jpg">

## Create a New Span in ```home_activities.py```
```py
from opentelemetry import trace

tracer = trace.get_tracer("tracer.name.here")
```

NOTE: Rename 'trace.name.here' replace it with 'home.activities'
- It's best practice to name it after the module/service it is being used for.



Add the following under def run within ```home_activities.py```

```py
with tracer.start_as_current_span("http-handler"):
```

NOTE: Rename 'http-handler' to name the span.

Found code to add from: https://docs.honeycomb.io/getting-data-in/opentelemetry/python/

<img src="./assets/week2/double-span-trace.jpg">

<img src="./assets/week2/double-span-trace-2.jpg">


# AWS X-ray
## Add & Install Dependencies
Add the following to ```requirements.txt```

```py
aws-xray-sdk
```

Change directories to backend-flask then install dependencies:

```
cd backend-flask
pip install -r requirements.txt
```


## Add to ```app.py```
```py
from aws_xray_sdk.core import xray_recorder
from aws_xray_sdk.ext.flask.middleware import XRayMiddleware

xray_url = os.getenv("AWS_XRAY_URL")
xray_recorder.configure(service='backend-flask', dynamic_naming=xray_url)
XRayMiddleware(app, xray_recorder)
```
## Add `aws/json/xray.json`

```json
{
  "SamplingRule": {
      "RuleName": "Cruddur",
      "ResourceARN": "*",
      "Priority": 9000,
      "FixedRate": 0.1,
      "ReservoirSize": 5,
      "ServiceName": "backend-flask",
      "ServiceType": "*",
      "Host": "*",
      "HTTPMethod": "*",
      "URLPath": "*",
      "Version": 1
  }
}
```

## Create a Group to Create X-ray Trace
Run the following from within ```backend-flask```

```sh
FLASK_ADDRESS="https://4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}"
aws xray create-group \
   --group-name "Cruddur" \
   --filter-expression "service(\"backend-flask\")"
```

- I ran into an issue while trying to create a group for X-ray traces due to leaving off an additional " at the end of the command.

<img src="./assets/week2/create-xray-group.jpg">

## Create a Sampling Rule
Sampling will allow you to determine what information you will see.
- This can help reduce spend.

Run the following from the terminal:

```sh
aws xray create-sampling-rule --cli-input-json file://aws/json/xray.json
```

## Add Daemon Service to ```docker-compose.yml```

```yml
  xray-daemon:
    image: "amazon/aws-xray-daemon"
    environment:
      AWS_ACCESS_KEY_ID: "${AWS_ACCESS_KEY_ID}"
      AWS_SECRET_ACCESS_KEY: "${AWS_SECRET_ACCESS_KEY}"
      AWS_REGION: "us-east-1"
    command:
      - "xray -o -b xray-daemon:2000"
    ports:
      - 2000:2000/udp
```

We need to add these two env vars to our backend-flask in our `docker-compose.yml` file

```yml
      AWS_XRAY_URL: "*4567-${GITPOD_WORKSPACE_ID}.${GITPOD_WORKSPACE_CLUSTER_HOST}*"
      AWS_XRAY_DAEMON_ADDRESS: "xray-daemon:2000"
```



# Homework Challenges
# Instrument Honeycomb for the frontend-application to observe network latency between frontend and backend[HARD]
## Set the Service Name
```sh
export HONEYCOMB_API_KEY=""
export HONEYCOMB_SERVICE_NAME="frontend-react-js"
gp env HONEYCOMB_API_KEY=""
gp env HONEYCOMB_SERVICE_NAME="frontend-react-js"
```

Note: I'm unsure if this is going to work as my API key and Env Var for backend-flask are now replaced with the API Key and Env Var for frontend-react-js.

<img src="./assets/week2/set-frontend-api.jpg">

## Set Env Vars for ```frontend-react-js``` in ```docker-compose ```
Add the following to the backend-flask service.

```docker
OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
OTEL_SERVICE_NAME: "frontend-react-js"
```

## Instrumentation Packages
Add the following to ```package-lock.json```

```sh
# not sure if the npm install --save is needed
# npm install --save
@opentelemetry/api
@opentelemetry/sdk-trace-web
@opentelemetry/exporter-trace-otlp-http
@opentelemetry/context-zone
```


## Create Initialization File
```js
// tracing.js
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { WebTracerProvider, BatchSpanProcessor } from '@opentelemetry/sdk-trace-web';
import { ZoneContextManager } from '@opentelemetry/context-zone';
import { Resource }  from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';

const exporter = new OTLPTraceExporter({
  url: 'https://<your collector endpoint>:443/v1/traces'
});
const provider = new WebTracerProvider({
  resource: new Resource({
    [SemanticResourceAttributes.SERVICE_NAME]: 'browser',
  }),
});
provider.addSpanProcessor(new BatchSpanProcessor(exporter));
provider.register({
  contextManager: new ZoneContextManager()
});
```


```js
// index.js
import './tracing.js'

// ...rest of the app's entry point code
```

# Add custom instrumentation to Honeycomb to add more attributes eg. UserId, Add a custom span
Resource: https://docs.honeycomb.io/getting-data-in/opentelemetry/python/


# Run custom queries in Honeycomb and save them later eg. Latency by UserID, Recent Traces
Resource: https://docs.honeycomb.io/working-with-your-data/queries/

## About Queries
Queries in HoneyComb consist of 6 clauses:
- Visualize: Visualize specific stats across events
- Where: Choose events based on additional criteria.
- Group By: Split events into groups based on the value of a specified attribute.
- Order By: Sort the results.
- Limit: Specify a limit on the number of results to return.
- Having: Filter results based on aggregate criteria.

Most queries output defaults to a time series and a summary table. Precise composition will depend on the composition of the queries you create:
    
- Specifying a visualize clause will cause a time series to be drawn representing the calculated value over time. 
    - Multiple visualize clauses wil result in multiple graphs, one for each calculation.
- Specifying a group by clause will result in the time series drawing multiple lines, one for each group.
    - The summary table will contain a single row for each unique group.
- Leaving visualize blank will result in raw event data being returned without any summarization.

## Create a New Query
I created 2 new queries to save for later.
1. Based on status codes not equal to 200.
2. Based on the backend-flask service name where the trace.parent_id doesn't exist, grouping by user agent and displayed in descending order.


From within HoneyComb, click on New Query.

<img src="./assets/week2/honeycomb-new-query.jpg">

- Select the desired Visualize option
- Select the desired Where option
- Select the desired Group By option

Then click Run Query

<img src="./assets/week2/honeycomb-status-code-query.jpg">

I created an addition query using the Heatmap Visualize option:

<img src="./assets/week2/honeycomb-heatmap-query.jpg">

To find these queries again to run, you can click on the History tab on the left side of the screen.

<img src="./assets/week2/honeycomb-query-history.jpg">