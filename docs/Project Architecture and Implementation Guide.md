# Project Architecture and Implementation Guide

## Overview

The `ds-practice-2024` project simulates a distributed system for an online bookstore. It features a frontend service, an orchestrator service, and three backend microservices: fraud detection, transaction verification, and suggestions. The system employs REST for frontend-backend communication and gRPC for inter-service communication. A significant feature of this system is its use of a priority queue in the order processing mechanism, allowing for more sophisticated order handling based on defined criteria.

## Architecture

### Components

- **Frontend Service**: Interacts with users, collecting order requests and displaying order statuses and book suggestions.
- **Orchestrator Service**: Serves as the central hub for processing requests from the frontend. It communicates with backend services and consolidates results.
- **Fraud Detection Service**: Analyzes transactions to identify potential fraud.
- **Transaction Verification Service**: Confirms the validity of transactions.
- **Suggestions Service**: Provides book recommendations based on user preferences.
- **Order Queue Service**: Manages order processing using a priority queue, ensuring that orders are processed based on priority criteria.
- **Order Executor Service**: Responsible for executing orders. It includes a leader election mechanism to ensure that only the elected leader can dequeue and execute orders.

### Communication

- **REST API**: Facilitates communication between the frontend and the orchestrator.
- **gRPC**: Enables communication between the orchestrator and backend services, as well as within backend services themselves.

## Implementation Tasks

### REST Implementation

- Implement REST API endpoints in the orchestrator service as per the OpenAPI specification in `utils/api/bookstore.yaml`.

### Orchestrator Service

- Implement logic to deploy worker threads for parallel processing of requests to backend services using `ThreadPoolExecutor`.

### Backend Microservices

- Implement dummy logic for fraud detection on port 50051.
- Implement simple logic for transaction verification on port 50052.
- Implement logic for returning book suggestions on port 50053.

### gRPC Communication Setup

- Establish gRPC channels in the orchestrator to communicate with backend services.
- Define gRPC services and messages based on `.proto` files in `utils/pb`.

### Priority Queue in Order Processing

- Modify the Order Queue Service to use a priority queue for managing orders. Orders are prioritized based on criteria such as the number of books in an order, with orders containing more books given higher priority.
- Use Python's `heapq` module to implement the priority queue functionality.
- Ensure thread safety when enqueuing and dequeuing orders by using locks.

### Leader Election in Order Executor Service

- Implement a leader election mechanism in the Order Executor Service to ensure that only the elected leader can dequeue and execute orders.
- After executing an order, trigger a re-election to allow for dynamic leadership.

### System Logging

- Implement logging across services to capture key events such as request reception, thread spawning, and response sending.

## Docker and Docker Compose

- Containerize each service using Docker, with configurations specified in `docker-compose.yaml`.
- Use Docker Compose to orchestrate the services, ensuring they are networked together for communication.

## Conclusion

This guide provides a comprehensive overview of the architecture and implementation steps for the `ds-practice-2024` project. It highlights the system's use of REST and gRPC for communication, the implementation of a priority queue for order processing, and the dynamic leader election mechanism in the Order Executor Service.