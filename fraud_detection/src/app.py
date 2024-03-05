import logging
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
# FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
# utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
# sys.path.insert(0, utils_path)
# import fraud_detection_pb2 as fraud_detection
# import fraud_detection_pb2_grpc as fraud_detection_grpc

import grpc
from concurrent import futures

from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FraudDetectionServiceImpl(fraud_detection_pb2_grpc.FraudDetectionServiceServicer):
    def CheckFraud(self, request, context):
        # Enhanced logic: Check if the amount is above a certain threshold
        fraud_threshold = 10000  # Example threshold for fraud detection
        if request.amount > fraud_threshold:
            logging.info(f"Transaction detected as fraud. Amount: {request.amount}")
            return fraud_detection_pb2.FraudCheckResponse(is_fraud=True)
        else:
            logging.info(f"Transaction detected as not fraud. Amount: {request.amount}")
            return fraud_detection_pb2.FraudCheckResponse(is_fraud=False)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServiceServicer_to_server(
        FraudDetectionServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Fraud Detection Service running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()