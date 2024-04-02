import grpc
import threading
from concurrent import futures
import sys
import os
import heapq

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path_order_executor = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_executor'))
sys.path.insert(0, utils_path_order_executor)

utils_path_order_queue = os.path.abspath(os.path.join(FILE, '../../../utils/pb/order_queue'))
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

    def ClearCurrentLeader(self, request, context):
        with self.leader_lock:
            self.current_leader = None
            return order_queue_pb2.ClearLeaderResponse() 

    def Enqueue(self, request, context):
        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("order_queue_service")

        # Determine the priority of the order
        # The priority is related to the number of books (more books = higher priority)
        # Heapq is a min heap, so we use negative to simulate a max heap behavior
        priority = -len(request.bookTitles)

        # Use a tuple (priority, request, vc) to maintain the queue
        with self.leader_lock:
            heapq.heappush(self.order_queue, (priority, request, vc))

        print(f"Order {request.orderId} enqueued with priority {priority}")
        return order_queue_pb2.OrderResponse(
            success=True, 
            message="Order enqueued successfully.",
            vector_clock=vc.to_proto(order_queue_pb2.VectorClock)
        )

    def Dequeue(self, request, context):
        with self.leader_lock:
            if request.executorId != self.current_leader:
                return order_queue_pb2.OrderRequest()
            if self.order_queue:
                order, vc = self.order_queue.pop(0)
                vc.increment("order_queue_service")
                print(f"Order {order.orderId} dequeued")
                return order_queue_pb2.OrderRequest(
                    orderId=order.orderId,
                    userId=order.userId,
                    bookTitles=order.bookTitles,
                    vector_clock=vc.to_proto(order_queue_pb2.VectorClock)
                )
            else:
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