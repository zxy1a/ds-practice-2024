import grpc
import threading
from concurrent import futures
import sys
import os
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
base_path = os.path.abspath(os.path.join(FILE, '../../../'))

utils_path_order_executor = os.path.join(base_path, 'utils/pb/order_executor')
sys.path.insert(0, utils_path_order_executor)

utils_path_order_queue = os.path.join(base_path, 'utils/pb/order_queue')
sys.path.insert(0, utils_path_order_queue)

from utils.pb.order_queue import order_queue_pb2, order_queue_pb2_grpc
from utils.vector_clock import VectorClock  

class OrderQueueService(order_queue_pb2_grpc.OrderQueueServicer):
    def __init__(self):
        self.order_queue = []
        self.current_leader = None
        self.leader_lock = threading.Lock()

    def ElectLeader(self, request, context):
        with self.leader_lock:
            if not self.current_leader:
                self.current_leader = request.executorId
                return order_queue_pb2.ElectionResponse(isLeader=True)
            else:
                return order_queue_pb2.ElectionResponse(isLeader=request.executorId == self.current_leader)

    def Enqueue(self, request, context):
        # Increment the Vector Clock for enqueue operation
        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("order_queue_service")

        # Append the order along with its Vector Clock to the queue
        self.order_queue.append((request, vc))

        print(f"Order {request.orderId} enqueued")
        return order_queue_pb2.OrderResponse(
            success=True, 
            message="Order enqueued successfully.",
            vector_clock=vc.to_proto(order_queue_pb2.VectorClock)  # Return the updated Vector Clock
        )

    def Dequeue(self, request, context):
        if self.order_queue:
            order, vc = self.order_queue.pop(0)
            vc.increment("order_queue_service")  # Increment the Vector Clock for dequeue operation

            print(f"Order {order.orderId} dequeued")
            # Return the dequeued order with the updated Vector Clock
            return order_queue_pb2.OrderRequest(
                orderId=order.orderId,
                userId=order.userId,
                bookTitles=order.bookTitles,
                vector_clock=vc.to_proto(order_queue_pb2.VectorClock)
            )
        else:
            # Return an empty response if the queue is empty
            return order_queue_pb2.OrderRequest()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_queue_pb2_grpc.add_OrderQueueServicer_to_server(OrderQueueService(), server)
    server.add_insecure_port('[::]:50054')  
    server.start()
    print("Order Queue Server running on port 50054")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()