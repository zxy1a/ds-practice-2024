import grpc
from concurrent import futures
import logging
import sys
import os
# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path)

from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

order_cache = {}

def cache_order_data(order_id, data):
    order_cache[order_id] = data

class TransactionVerificationServiceImpl(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):

        # Extract the order ID from the request (assuming it's part of the request)
        order_id = request.orderID

        # Cache the incoming order data
        cache_order_data(order_id, request)

        # Extract the vector clock from the request
        vector_clock = request.vector_clock

        # Update the vector clock for this service
        service_id = "transaction_verification_service"
        if service_id in vector_clock.entries:
            vector_clock.entries[service_id] += 1
        else:
            vector_clock.entries[service_id] = 1

        logging.info(f"OrderID {request.orderID} - Current Vector Clock: {dict(vector_clock.entries)}")

        card = request.creditCard

        card_number = card.number.replace(" ", "").replace("-", "")
        if len(card_number) == 16 and card_number.isdigit():
            logging.info(f"Card number is valid")
            return transaction_verification_pb2.TransactionVerificationResponse(
                is_valid=True, 
                message="Approved",
                vector_clock=vector_clock
            )
        else:
            logging.warning(f"Card number is invalid")
            return transaction_verification_pb2.TransactionVerificationResponse(
                is_valid=False, 
                message="Denied",
                vector_clock=vector_clock
            )

    def VerifyCreditCardFormat(self, request, context):
        vector_clock = request.vector_clock.entries
        service_id = "transaction_verification_service"
        if service_id in vector_clock.entries:
            vector_clock.entries[service_id] += 1
        else:
            vector_clock.entries[service_id] = 1
        card_number = request.creditCard.number.replace(" ", "").replace("-", "")
        if len(card_number) == 16 and card_number.isdigit():
            return transaction_verification_pb2.VerifyCreditCardFormatResponse(
                is_valid=True,
                message="Credit card format is valid",
                vector_clock=transaction_verification_pb2.VectorClock(entries=vector_clock)
            )
        else:
            return transaction_verification_pb2.VerifyCreditCardFormatResponse(
                is_valid=False,
                message="Credit card format is invalid",
                vector_clock=transaction_verification_pb2.VectorClock(entries=vector_clock)
            )

    def VerifyMandatoryUserData(self, request, context):
        # Extract the vector clock from the request
        vector_clock = request.vector_clock.entries
        service_id = "transaction_verification_service"
        if service_id in vector_clock.entries:
            vector_clock.entries[service_id] += 1
        else:
            vector_clock.entries[service_id] = 1

        # Verify if mandatory user data (name, contact, address) is filled in
        user = request.user
        if not all([user.name, user.contact, user.address]):
            return transaction_verification_pb2.VerifyMandatoryUserDataResponse(
                is_valid=False,
                message="Mandatory user data is missing",
                vector_clock=transaction_verification_pb2.VectorClock(entries=vector_clock)
            )
        else:
            return transaction_verification_pb2.VerifyMandatoryUserDataResponse(
                is_valid=True,
                message="Mandatory user data is valid",
                vector_clock=transaction_verification_pb2.VectorClock(entries=vector_clock)
            )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    transaction_verification_pb2_grpc.add_TransactionVerificationServicer_to_server(
        TransactionVerificationServiceImpl(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logging.info("Transaction Verification Service running on port 50052")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
