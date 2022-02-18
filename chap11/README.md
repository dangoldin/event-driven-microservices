# Chapter 10: Basic Producer and Consumer Microservices

> Basic consumer clients do not include any event scheduling, watermarks, mechanisms for materialization, changelogs, or horizontal scaling of processing instances with local state stores.

> The entire workflow of the bounded context is contained within the code of the single microservice application, keeping the responsibilities of the microservice localized and easy to understand.

Notes:

- Chapter 11 is Heavyweight Framework Microservices
- Chapter 12 is Lightweight Framework Microservices

## Use Cases

### 1. Integration with Existing and Legacy Systems

![Backend -> Batch -> Frontend](/img/backend-batch-frontend.png "Backend -> Batch -> Frontend")

Can be turned into:

![Backend -> Microservice -> Frontend](/img/backend-batch-frontend-v2.png "Backend -> Microservice -> Frontend")

- The backend and frontend systems are loosely coupled.
- The two systems operate as before, just bolt on event production to the backend.
- The database powering the frontend now receives events as they arrive rather than waiting for the batch process.

### 2. Stateful Business Logic That Isn’t Reliant Upon Event Order

![Book publishing](/img/book-publishing.png "Book publishing")

- Different events that all need to happen for something to trigger.

### 3. When the Data Layer Does Much of the Work

- Basically just persisting to a data store.

### 4. Independent Scaling of the Processing and Data Layer

- Allow you to scale processing based on event volume but keep the data store consistent.

## Hybrid BPC Applications with External Stream Processing

### Example: Using an External Stream-Processing Framework to Join Event Streams

![External stream join](/img/join.png "External stream join")

![External stream join hybrid](/img/hybrid.png "External stream join hybrid")

## Demos

### Start Kafka

```bash
~ brew install redpanda-data/tap/redpanda
~ rpk container start -n 3
~ rpk cluster info --brokers 127.0.0.1:61824,127.0.0.1:61829,127.0.0.1:61830
~ rpk topic create in --brokers 127.0.0.1:61824,127.0.0.1:61829,127.0.0.1:61830
~ rpk topic create in2 --brokers 127.0.0.1:61824,127.0.0.1:61829,127.0.0.1:61830
~ rpk topic create out --brokers 127.0.0.1:61824,127.0.0.1:61829,127.0.0.1:61830
```

### VS Code Kafka

https://github.com/jlandersen/vscode-kafka/blob/master/docs/README.md
