import grpc
from concurrent import futures
import logging

from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class TransactionVerificationServiceImpl(transaction_verification_pb2_grpc.TransactionVerificationServicer):
    def VerifyTransaction(self, request, context):

        card = request.creditCard

        card_number = card.replace(" ", "").replace("-", "")
        if len(card_number) == 16 and card_number.isdigit():
            logging.info(f"Card number is valid")
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=True, message="Approved")
        else:
            logging.warning(f"Card number is invalid")
            return transaction_verification_pb2.TransactionVerificationResponse(is_valid=False, message="Denied")


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
