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
import datetime
from concurrent import futures

from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FraudDetectionServiceImpl(fraud_detection_pb2_grpc.FraudDetectionServicer):
    def CheckFraud(self, request, context):
        message = ""
        expiry_date = datetime.datetime.strptime(request.expirationDate, "%m/%d")
        current_date = datetime.datetime.now()
        six_months_later = current_date + datetime.timedelta(days=180)
        if expiry_date > six_months_later:
            logging.info("Transaction detected as fraud")
            return fraud_detection_pb2.FraudDetectionResponse(is_fraud=True, message="Card is expired")
        else:
            logging.info(f"Transaction detected as not fraud")
            return fraud_detection_pb2.FraudDetectionResponse(is_fraud=False, message="Approved")


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
