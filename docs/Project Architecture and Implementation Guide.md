# Project Architecture and Implementation Guide

## Overview
The `ds-practice-2024` project is designed to simulate a distributed system for an online bookstore. It comprises a frontend service, an orchestrator service, and three backend microservices: fraud detection, transaction verification, and suggestions. The system uses REST for frontend-backend communication and gRPC for inter-service communication.

## Architecture

### Components

- **Frontend Service**: Interacts with users and sends requests to the orchestrator service.
- **Orchestrator Service**: Acts as a central point that processes requests from the frontend, communicates with backend services, and consolidates results.
- **Fraud Detection Service**: Analyzes transactions to detect fraudulent activities.
- **Transaction Verification Service**: Verifies the validity of transactions.
- **Suggestions Service**: Provides book suggestions based on user preferences.

### Communication

- **REST API**: Used between the frontend and the orchestrator.
- **gRPC**: Used for communication between the orchestrator and backend services.

## Implementation Tasks

### REST Implementation

- Implement REST API endpoints in the orchestrator service based on the OpenAPI specification found in `utils/api/bookstore.yaml`.
- Example endpoint in the orchestrator for handling checkout requests:


```python
if responses['fraud'][0]:  # is_fraud
    order_status = 'Order Rejected due to fraud detection'
elif not responses['transaction'][0]:  # is_valid
    order_status = 'Order Rejected due to transaction verification failure'
else:
    order_status = 'Order Approved'
```


### Orchestrator Service

- Implement logic to deploy worker threads for parallel processing of requests to backend services.
- Use `ThreadPoolExecutor` for managing worker threads.

### Backend Microservices

- **Fraud Detection Service** (`port 50051`): Implement dummy logic for fraud detection.
- **Transaction Verification Service** (`port 50052`): Implement simple logic for transaction verification.
- **Suggestions Service** (`port 50053`): Implement logic to return book suggestions.

### gRPC Communication Setup

- Establish gRPC channels in the orchestrator to communicate with backend services.
- Define gRPC services and messages based on `.proto` files in `utils/pb`.

### Results Consolidation

- In the orchestrator, combine results from backend services and construct a response based on the outcome.
- Example logic for consolidating results:


```python
if responses['fraud'][0]:  # is_fraud
    order_status = 'Order Rejected due to fraud detection'
elif not responses['transaction'][0]:  # is_valid
    order_status = 'Order Rejected due to transaction verification failure'
else:
    order_status = 'Order Approved'
```


### System Logging

- Add logging across services to capture key events such as request reception, thread spawning, and response sending.

## Docker and Docker Compose

- Each service is containerized using Docker, with configuration specified in `docker-compose.yaml`.
- Services are orchestrated using Docker Compose, ensuring they are networked together for communication.

## Conclusion

This guide outlines the architecture and implementation steps for the `ds-practice-2024` project, focusing on REST and gRPC communication, service logic, and results consolidation.
