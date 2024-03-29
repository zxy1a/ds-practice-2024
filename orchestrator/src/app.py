import sys
import os
import grpc
import logging
import uuid

FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path_fraud = os.path.abspath(os.path.join(FILE, '../../../utils/pb/fraud_detection'))
sys.path.insert(0, utils_path_fraud)

utils_path_transactionverfication = os.path.abspath(os.path.join(FILE, '../../../utils/pb/transaction_verification'))
sys.path.insert(0, utils_path_transactionverfication)

utils_path_suggestions = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path_suggestions)
from flask_cors import CORS
from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2
from utils.pb.suggestions import suggestions_pb2_grpc, suggestions_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor


# Establish gRPC connection
def detect_fraud(number, expiration_date):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        response = stub.FraudDetection(
            fraud_detection_pb2.FraudDetectionRequest(number=number, expirationDate=expiration_date))
        return response.is_fraud, response.reason


def verify_transaction(title, user, credit_card):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        # Construct CreditCard message
        credit_card_message = transaction_verification_pb2.CreditCard(
            number=credit_card['number'],
            expirationDate=credit_card['expirationDate'],
            cvv=credit_card.get('cvv', '')
        )
        # Construct User message
        user_message = transaction_verification_pb2.User(
            name=user,
            contact=''
        )
        response = stub.VerifyTransaction(
            transaction_verification_pb2.TransactionVerificationRequest(
                title=title,
                user=user_message,
                creditCard=credit_card_message
            )
        )
        return response.is_valid, response.message


def suggestions(title, author):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsStub(channel)
        response = stub.BookSuggestions(suggestions_pb2.SuggestionsRequest(title=title, author=author))
        return response.titles


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
# Create a simple Flask app.
app = Flask(__name__)
# Enable CORS for the app.
CORS(app)


@app.route('/checkout', methods=['POST'])
def checkout():
    request_data = request.json
    responses = {}
    order_id = str(uuid.uuid4())

    with ThreadPoolExecutor(max_workers=3) as executor:

        first_item = request_data['items'][0] if 'items' in request_data and len(request_data['items']) > 0 else None
        title = first_item['name'] if first_item else None

        user_info = request_data.get('user', {})
        user_name = user_info.get('name', '')
        user_contact = user_info.get('contact', '')

        fraud_future = executor.submit(
            detect_fraud,
            request_data['creditCard']['number'],
            request_data['creditCard']['expirationDate']
        )
        transaction_future = executor.submit(
            verify_transaction,
            title,
            user_name,
            request_data['creditCard']
        )
        suggestions_future = executor.submit(
            suggestions,
            title,
            ''
        )

        responses['fraud'] = fraud_future.result()
        responses['transaction'] = transaction_future.result()
        responses['suggestions'] = suggestions_future.result()

    # Process responses
    if not responses['fraud'][0] and responses['transaction'][0]:  # if not fraud and transaction is valid
        order_status = 'Order Approved'
        suggested_books = [{'title': title} for title in responses['suggestions']]
    else:
        order_status = 'Order Rejected'
        suggested_books = []

        # Construct the response
    response = {
        'orderId': order_id,
        'status': order_status,
        'suggestedBooks': suggested_books if order_status == 'Order Approved' else []
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
