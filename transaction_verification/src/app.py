import grpc
from concurrent import futures
import logging

from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TransactionVerificationServiceImpl(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):
        # Define the transaction amount limit
        MIN_AMOUNT = 1.0
        MAX_AMOUNT = 10000.0

        # Check if the transaction amount is within the limits
        if MIN_AMOUNT <= request.amount <= MAX_AMOUNT:
            logging.info(f"Transaction amount {request.amount} is within the allowed limits.")
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True)
        else:
            logging.warning(f"Transaction amount {request.amount} is outside the allowed limits.")
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False)


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
