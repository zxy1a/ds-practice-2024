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

from utils.vector_clock import VectorClock
from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class FraudDetectionServiceImpl(fraud_detection_pb2_grpc.FraudDetectionServicer):

    def CheckUserDataForFraud(self, request, context):

        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("fraud_detection_service")

        # Reject if user name is empty or contact is missing
        if not request.user.name or not request.user.contact:
            # Convert the VectorClock instance back to the protobuf format for the response
            updated_vector_clock = vc.to_proto(fraud_detection_pb2.VectorClock)
            return fraud_detection_pb2.CheckUserDataResponse(
                is_fraud=True,
                reason="Missing user name or contact",
                vector_clock=updated_vector_clock
            )

        updated_vector_clock = vc.to_proto(fraud_detection_pb2.VectorClock)
        return fraud_detection_pb2.CheckUserDataResponse(
            is_fraud=False,
            reason="User data looks good",
            vector_clock=updated_vector_clock
        )

    def CheckCreditCardForFraud(self, request, context):

        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("fraud_detection_service")

        logging.info(f"OrderID {request.orderID} - Current Vector Clock: {vc.get_clock()}")

        expiry_date = datetime.datetime.strptime(request.expirationDate, "%m/%y")
        current_date = datetime.datetime.now()
        if expiry_date < current_date:
            logging.info("Transaction detected as a fraud due to expired card")
            # Include the updated vector clock in the response
            updated_vector_clock = vc.to_proto(fraud_detection_pb2.VectorClock)
            return fraud_detection_pb2.FraudDetectionResponse(
                is_fraud=True,
                reason="Card is expired",
                vector_clock=updated_vector_clock
            )
        else:
            logging.info(f"Transaction detected no fraud")
            # Include the updated vector clock in the response
            updated_vector_clock = vc.to_proto(fraud_detection_pb2.VectorClock)
            return fraud_detection_pb2.FraudDetectionResponse(
                is_fraud=False,
                reason="Approved",
                vector_clock=updated_vector_clock
            )


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
