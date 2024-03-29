import logging
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path)

import grpc
import datetime
from concurrent import futures

from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FraudDetectionServiceImpl(fraud_detection_pb2_grpc.FraudDetectionServicer):
    def FraudDetection(self, request, context):
        expiry_date = datetime.datetime.strptime(request.expirationDate, "%m/%y")
        current_date = datetime.datetime.now()
        if expiry_date < current_date:
            logging.info("Transaction detected as a fraud")
            return fraud_detection_pb2.FraudDetectionResponse(is_fraud=True, reason="Card is expired")
        else:
            logging.info(f"Transaction detected no fraud")
            return fraud_detection_pb2.FraudDetectionResponse(is_fraud=False, reason="Approved")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fraud_detection_pb2_grpc.add_FraudDetectionServicer_to_server(
        FraudDetectionServiceImpl(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logging.info("Fraud Detection Service running on port 50051")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
