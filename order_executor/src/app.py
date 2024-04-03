import grpc
import logging
from concurrent import futures
import socket
import sys
import os
import threading
import time

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")

utils_path_order_executor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path_order_executor)

utils_path_order_queue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
sys.path.insert(0, utils_path_order_queue)

from utils.pb.order_executor import order_executor_pb2, order_executor_pb2_grpc
from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc

class OrderExecutor(order_executor_pb2_grpc.OrderExecutorServicer):
    def __init__(self, executor_id):
        self.executor_id = executor_id

    def request_leadership(self):
        with grpc.insecure_channel('localhost:50054') as channel:
            order_queue_stub = order_queue_pb2_grpc.OrderQueueStub(channel)
            response = order_queue_stub.ElectLeader(order_queue_pb2.ElectionRequest(executorId=self.executor_id))
            return response.isLeader

    def ExecuteOrder(self, request, context):
        # First, request leadership
        if self.request_leadership():
            # If this instance is the leader, proceed to connect to the Order Queue service
            with grpc.insecure_channel('localhost:50054') as channel:
                order_queue_stub = order_queue_pb2_grpc.OrderQueueStub(channel)
                # Attempt to dequeue an order
                dequeued_order = order_queue_stub.Dequeue(order_queue_pb2.DequeueRequest())
                if dequeued_order.orderId:
                    print(f"Order {dequeued_order.orderId} is being executed...")
                    # Placeholder for actual execution logic
                    return order_executor_pb2.ExecuteOrderResponse(success=True, message="Order executed")
                else:
                    return order_executor_pb2.ExecuteOrderResponse(success=False, message="No order to execute")
        else:
            # If not the leader, do not attempt to execute orders
            print("Not the leader, skipping execution.")
            return order_executor_pb2.ExecuteOrderResponse(success=False, message="Not the leader")
        
    def poll_and_execute_orders(self):
        while True:
            is_leader = self.request_leadership()
            if is_leader:
                with grpc.insecure_channel('localhost:50054') as channel:
                    order_queue_stub = order_queue_pb2_grpc.OrderQueueStub(channel)
                    # Include executorId in DequeueRequest
                    dequeued_order_response = order_queue_stub.Dequeue(order_queue_pb2.DequeueRequest(executorId=self.executor_id))
                    if dequeued_order_response.orderId:
                        print(f"Order {dequeued_order_response.orderId} dequeued for execution")

                        # Release leadership before executing the order
                        order_queue_stub.ClearCurrentLeader(order_queue_pb2.ClearLeaderRequest())
                        print("Leadership released before executing the order.")

                        # Simulate order execution
                        print(f"Executing order {dequeued_order_response.orderId}")
                        print(f"Order {dequeued_order_response.orderId} executed")
                    else:
                        print("No orders to execute.")
            else:
                print("Not the leader, skipping execution.")
            time.sleep(5)


def serve():
    executor_id = socket.gethostname()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    executor_instance = OrderExecutor(executor_id)
    order_executor_pb2_grpc.add_OrderExecutorServicer_to_server(executor_instance, server)
    server.add_insecure_port('[::]:50055')
    server.start()
    print(f"Order Executor {executor_id} running on port 50055")
    # Start the polling in a background thread
    threading.Thread(target=executor_instance.poll_and_execute_orders, daemon=True).start()
    server.wait_for_termination()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    serve()

'''
Centralized Leader Election
In a centralized leader election algorithm, one node acts as the coordinator. This node is responsible for managing the election process and declaring the winner. The algorithm typically works as follows:
1. When a node determines that a new leader needs to be elected (e.g., due to the current leader failing or during system startup), it sends an election message to the coordinator.
2. The coordinator receives election messages from various nodes, decides which node should be the leader (usually based on a predetermined criterion such as the lowest node ID, highest available resources, etc.), and then informs all nodes in the system of the election result.
Why Choose Centralized Leader Election?
1. Simplicity: The centralized approach is straightforward to understand and implement. It does not require complex logic or state management across multiple nodes, making it easier to debug and maintain.
2. Efficiency for Small to Medium Systems: For systems with a small to medium number of nodes, a centralized leader election can be very efficient. The overhead of coordinating the election is minimal, and decisions can be made quickly.
3. Clear Coordination Point: Having a single point of coordination simplifies the process of managing elections and can also simplify other aspects of system management, such as configuration changes or updates.
4. Suitability for Your Use Case: Given that your system already involves a centralized Order Queue service, integrating a centralized leader election mechanism for the Order Executor service can align well with your existing architecture. The Order Queue service or a dedicated coordinator service can act as the central authority for leader election among Order Executor instances.
Considerations
Single Point of Failure: The main drawback of a centralized approach is that the coordinator becomes a single point of failure. If the coordinator node fails, the system may not be able to elect a new leader until the coordinator is restored. This issue can be mitigated by implementing failover mechanisms for the coordinator.
Scalability: As the system grows, the coordinator may become a bottleneck. However, for many applications, especially those with a moderate number of nodes, this is not an immediate concern.
Conclusion
A centralized leader election algorithm offers a good balance of simplicity, efficiency, and ease of implementation for your Order Executor service, especially considering the system's current architecture and scale. It provides a clear and straightforward way to manage leader election, making it a practical choice for ensuring mutual exclusion in order processing.
'''