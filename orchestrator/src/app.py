import sys
import os
import grpc
import logging
import CORS
from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2
from utils.pb.suggestions import suggestions_pb2_grpc, suggestions_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent import futures

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path_fraud = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path_fraud)

utils_path_transactionverfication = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path_transactionverfication)

utils_path_suggestions = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path_suggestions)

# Establish gRPC connection
def detect_fraud(number, expiration_date):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        response = stub.FraudDetection(fraud_detection_pb2.FraudDetectionRequest(number=number, expirationDate=expiration_date))
        return response.is_fraud, response.reason

def verify_transaction(title, user, credit_card):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        response = stub.VerifyTransaction(transaction_verification_pb2.TransactionVerificationRequest(title=title, user=user, creditCard=credit_card))
        return response.is_valid, response.message

def suggestions(title, author):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsStub(channel)
        response = stub.BookSuggestions(suggestions_pb2.SuggestionsRequest(title=title, author=author))
        return response.title



logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)


@app.route('/checkout', methods=['POST'])
def checkout():
    request_data = request.json
    responses = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_call = {
            executor.submit(detect_fraud): 'fraud',
            executor.submit(verify_transaction): 'transaction',
            executor.submit(suggestions): 'suggestions',
        }
        for future in as_completed(future_to_call):
            call_type = future_to_call[future]
            try:
                responses[call_type] = future.result()
            except Exception as exc:
                print(f'{call_type} generated an exception: {exc}')
                responses[call_type] = None

    # Example of how to process responses
    if responses['fraud'].is_fraud:
        order_status = 'Order Rejected due to fraud detection'
    elif not responses['transaction'].is_valid:
        order_status = 'Order Rejected due to transaction verification failure'
    else:
        order_status = 'Order Approved'
        # Assuming the suggestions service returns a list of book titles
        suggested_books = [{'title': book.title, 'author': book.author} for book in responses['suggestions'].bookTitles]

    # Construct the response
    response = {
        'orderId': request_data['orderId'],
        'status': order_status,
        'suggestedBooks': suggested_books if order_status == 'Order Approved' else []
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
