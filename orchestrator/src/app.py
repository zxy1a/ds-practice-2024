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
from utils.vector_clock import VectorClock
from utils.pb.fraud_detection import fraud_detection_pb2_grpc, fraud_detection_pb2
from utils.pb.suggestions import suggestions_pb2_grpc, suggestions_pb2
from utils.pb.transaction_verification import transaction_verification_pb2_grpc, transaction_verification_pb2
from flask import Flask, request, jsonify
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_order_details(request_data):
    first_item = request_data['items'][0] if 'items' in request_data and len(request_data['items']) > 0 else None
    title = first_item['name'] if first_item else None
    user_name = request_data.get('user', {}).get('name', '')
    credit_card = request_data.get('creditCard', {})
    return title, user_name, credit_card

def update_vector_clock(original_clock, response_clock):
    original_clock.merge(response_clock)
    return original_clock.get_clock()

def initialize_vector_clock():
    return VectorClock({"orchestrator": 1})

# Establish gRPC connection
def check_user_data_for_fraud(user, order_id, vector_clock):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        vector_clock_proto = vector_clock.to_proto(fraud_detection_pb2.VectorClock)
        
        user_data_request = fraud_detection_pb2.CheckUserDataRequest(
            orderID=order_id,
            user=fraud_detection_pb2.User(
                name=user['name'],
                contact=user.get('contact', ''),
                address=user.get('address', '')
            ),
            vector_clock=vector_clock_proto
        )
        response = stub.CheckUserDataForFraud(user_data_request)
        vector_clock.merge(VectorClock.from_proto(response.vector_clock).get_clock())
        
        return response.is_fraud, response.reason, vector_clock.get_clock()
    
def check_credit_card_for_fraud(credit_card, order_id, vector_clock):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        vector_clock_proto = vector_clock.to_proto(fraud_detection_pb2.VectorClock)
        
        credit_card_data_request = fraud_detection_pb2.CheckCreditCardForFraudRequest(
            orderID=order_id,
            creditCard=fraud_detection_pb2.CreditCard(
                number=credit_card['number'],
                expirationDate=credit_card['expirationDate']
            ),
            vector_clock=vector_clock_proto
        )
        response = stub.CheckCreditCardForFraud(credit_card_data_request)
        vector_clock.merge(VectorClock.from_proto(response.vector_clock).get_clock())
        
        return response.is_fraud, response.reason, vector_clock.get_clock()


def verify_credit_card_format(request_data, order_id, vector_clock):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        
        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(transaction_verification_pb2.VectorClock)
        
        # Constructing the CreditCard message
        credit_card_message = transaction_verification_pb2.CreditCard(
            number=request_data['creditCard']['number'],
            expirationDate=request_data['creditCard']['expirationDate'],
            cvv=request_data['creditCard']['cvv']
        )
        
        # Preparing the VerifyCreditCardFormatRequest
        verify_credit_card_format_request = transaction_verification_pb2.VerifyCreditCardFormatRequest(
            orderID=order_id,
            creditCard=credit_card_message,
            vector_clock=vector_clock_proto
        )
        
        # Sending the request to the TransactionVerification service
        response = stub.VerifyCreditCardFormat(verify_credit_card_format_request)
        
        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        updated_vector_clock = vector_clock.merge(response_clock.get_clock())
        
        return response.is_valid, response.message, updated_vector_clock
    
def verify_mandatory_user_data(request_data, order_id, vector_clock):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        
        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(transaction_verification_pb2.VectorClock)
        
        # Constructing the User message
        user_message = transaction_verification_pb2.User(
            name=request_data['user']['name'],
            contact=request_data['user']['contact'],
            address=f"{request_data['billingAddress']['street']}, {request_data['billingAddress']['city']}, {request_data['billingAddress']['state']}, {request_data['billingAddress']['zip']}, {request_data['billingAddress']['country']}"
        )
        
        # Preparing the VerifyMandatoryUserDataRequest
        verify_mandatory_user_data_request = transaction_verification_pb2.VerifyMandatoryUserDataRequest(
            orderID=order_id,
            user=user_message,
            vector_clock=vector_clock_proto
        )
        
        # Sending the request to the TransactionVerification service
        response = stub.VerifyMandatoryUserData(verify_mandatory_user_data_request)
        
        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        updated_vector_clock = vector_clock.merge(response_clock.get_clock())
        
        return response.is_valid, response.message, updated_vector_clock

def suggestions(title, author, order_id, vector_clock):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsStub(channel)

        # Convert the VectorClock instance to the protobuf format for the gRPC call
        vector_clock_proto = vector_clock.to_proto(suggestions_pb2.VectorClock)

        request = suggestions_pb2.SuggestionsRequest(
            orderID=order_id,
            title=title,
            author=author,
            vector_clock=vector_clock_proto
        )
        response = stub.BookSuggestions(request)

        # Update the vector clock with the response
        response_clock = VectorClock.from_proto(response.vector_clock)
        vector_clock.merge(response_clock.get_clock())
        
        # Return the list of suggested titles and the updated vector clock
        return response.titles, vector_clock.get_clock()


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
    vector_clock = initialize_vector_clock()
    order_status = 'Order Pending'
    suggested_books = []

    # Event a: Verify mandatory user data
    vector_clock.increment("transaction_verification")
    is_valid, message, vc_after_a = verify_mandatory_user_data(request_data, order_id, vector_clock)
    if not is_valid:
        return jsonify({"error": "Mandatory user data is missing", "message": message}), 400
    vector_clock.merge(vc_after_a)

    # Event b: Verify credit card format
    vector_clock.increment("transaction_verification")
    is_valid, message, vc_after_b = verify_credit_card_format(request_data, order_id, vector_clock)
    if not is_valid:
        return jsonify({"error": "Credit card format is incorrect", "message": message}), 400
    vector_clock.merge(vc_after_b)

    # Event d: Check credit card data for fraud
    vector_clock.increment("fraud_detection")
    is_fraud, reason, vc_after_d = check_credit_card_for_fraud(request_data.get('creditCard', {}), order_id, vector_clock)
    if is_fraud:
        return jsonify({"error": "Fraud detected in credit card data", "reason": reason}), 400
    vector_clock.merge(vc_after_d)

    # Event c: Check user data for fraud
    vector_clock.increment("fraud_detection")
    is_fraud, reason, vc_after_c = check_user_data_for_fraud(request_data.get('user', {}), order_id, vector_clock)
    if is_fraud:
        return jsonify({"error": "Fraud detected in user data", "reason": reason}), 400
    vector_clock.merge(vc_after_c)

    # Event e: Generate book suggestions
    vector_clock.increment("suggestions")
    title, author = extract_order_details(request_data)[:2]  # Assuming extract_order_details returns title and author among other details
    suggested_titles, vc_after_e = suggestions(title, author, order_id, vector_clock)
    if suggested_titles:
        suggested_books = [{'title': title} for title in suggested_titles]
        order_status = 'Order Approved'
    else:
        order_status = 'Order Rejected'
    vector_clock.merge(vc_after_e)

    # Construct the response
    response = {
        'orderId': order_id,
        'status': order_status,
        'vectorClock': vector_clock.get_clock(),  # Include the final state of the vector clock
        'suggestedBooks': suggested_books if order_status == 'Order Approved' else [],
        'message': "Order processed successfully" if order_status == 'Order Approved' else "Order processing failed"
    }

    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
