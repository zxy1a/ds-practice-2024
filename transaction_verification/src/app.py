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

from utils.vector_clock import VectorClock
from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

order_cache = {}

def cache_order_data(order_id, data):
    order_cache[order_id] = data

class TransactionVerificationServiceImpl(transaction_verification_pb2_grpc.TransactionVerificationServicer):

    def VerifyCreditCardFormat(self, request, context):

        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("transaction_verification_service")

        card_number = request.creditCard.number.replace(" ", "").replace("-", "")
        if len(card_number) == 16 and card_number.isdigit():
            updated_vector_clock = vc.to_proto(transaction_verification_pb2.VectorClock)
            return transaction_verification_pb2.VerifyCreditCardFormatResponse(
                is_valid=True,
                message="Credit card format is valid",
                vector_clock=updated_vector_clock
            )
        else:
            updated_vector_clock = vc.to_proto(transaction_verification_pb2.VectorClock)
            return transaction_verification_pb2.VerifyCreditCardFormatResponse(
                is_valid=False,
                message="Credit card format is invalid",
                vector_clock=updated_vector_clock
            )

    def VerifyMandatoryUserData(self, request, context):

        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("transaction_verification_service")

        # Verify if mandatory user data (name, contact, address) is filled in
        user = request.user
        if not all([user.name, user.contact, user.address]):
            updated_vector_clock = vc.to_proto(transaction_verification_pb2.VectorClock)
            return transaction_verification_pb2.VerifyMandatoryUserDataResponse(
                is_valid=False,
                message="Mandatory user data is missing",
                vector_clock=updated_vector_clock
            )
        else:
            updated_vector_clock = vc.to_proto(transaction_verification_pb2.VectorClock)
            return transaction_verification_pb2.VerifyMandatoryUserDataResponse(
                is_valid=True,
                message="Mandatory user data is valid",
                vector_clock=updated_vector_clock
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
