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
from concurrent.futures import ThreadPoolExecutor, as_completed

def extract_order_details(request_data):
    first_item = request_data['items'][0] if 'items' in request_data and len(request_data['items']) > 0 else None
    title = first_item['name'] if first_item else None
    user_name = request_data.get('user', {}).get('name', '')
    credit_card = request_data.get('creditCard', {})
    return title, user_name, credit_card

def update_vector_clock(original_clock, response_clock):
    for key, value in response_clock.items():
        original_clock[key] = max(original_clock.get(key, 0), value)
    return original_clock

def initialize_vector_clock():
    return {"orchestrator": 1}

# Establish gRPC connection
def detect_fraud(user, credit_card, order_id, vector_clock):
    with grpc.insecure_channel('fraud_detection:50051') as channel:
        stub = fraud_detection_pb2_grpc.FraudDetectionStub(channel)
        
        # Prepare the user data for the CheckUserDataForFraud call
        user_data_request = fraud_detection_pb2.CheckUserDataRequest(
            orderID=order_id,
            user=fraud_detection_pb2.User(
                name=user['name'],
                contact=user.get('contact', ''),  
                address=user.get('address', '')  
            ),
            vector_clock=fraud_detection_pb2.VectorClock(entries=vector_clock)
        )
        user_data_response = stub.CheckUserDataForFraud(user_data_request)
        
        # If user data is flagged as fraud, return immediately
        if user_data_response.is_fraud:
            return True, user_data_response.reason, user_data_response.vector_clock.entries
        
        # Prepare the credit card data for the CheckCreditCardForFraud call
        credit_card_data_request = fraud_detection_pb2.FraudDetectionRequest(
            orderID=order_id,
            number=credit_card['number'],
            expirationDate=credit_card['expirationDate'],
            vector_clock=fraud_detection_pb2.VectorClock(entries=vector_clock)
        )
        credit_card_data_response = stub.CheckCreditCardForFraud(credit_card_data_request)
        
        # Return the result of the credit card fraud check with the updated vector clock
        updated_vector_clock = {key: value for key, value in credit_card_data_response.vector_clock.entries.items()}
        return credit_card_data_response.is_fraud, credit_card_data_response.reason, updated_vector_clock


def verify_transaction(request_data, order_id, vector_clock):
    with grpc.insecure_channel('transaction_verification:50052') as channel:
        stub = transaction_verification_pb2_grpc.TransactionVerificationStub(channel)
        
        # Constructing the CreditCard message
        credit_card_message = transaction_verification_pb2.CreditCard(
            number=request_data['creditCard']['number'],
            expirationDate=request_data['creditCard']['expirationDate'],
            cvv=request_data['creditCard']['cvv']
        )
        
        # Constructing the User message
        user_message = transaction_verification_pb2.User(
            name=request_data['user']['name'],
            contact=request_data['user']['contact'],
            address=f"{request_data['billingAddress']['street']}, {request_data['billingAddress']['city']}, {request_data['billingAddress']['state']}, {request_data['billingAddress']['zip']}, {request_data['billingAddress']['country']}"
        )
        
        # Preparing the TransactionVerificationRequest
        transaction_verification_request = transaction_verification_pb2.TransactionVerificationRequest(
            orderID=order_id,
            title=request_data['items'][0]['name'] if request_data['items'] else 'No title',  
            user=user_message,
            creditCard=credit_card_message,
            vector_clock=transaction_verification_pb2.VectorClock(entries=vector_clock)
        )
        
        # Sending the request to the TransactionVerification service
        response = stub.VerifyTransaction(transaction_verification_request)
        
        # Updating the vector clock with the response
        updated_vector_clock = {key: value for key, value in response.vector_clock.entries.items()}
        
        return response.is_valid, response.message, updated_vector_clock


def suggestions(title, author, order_id, vector_clock):
    with grpc.insecure_channel('suggestions:50053') as channel:
        stub = suggestions_pb2_grpc.SuggestionsStub(channel)
        vector_clock_entries = {key: suggestions_pb2.VectorClock.Entry(value=value) for key, value in vector_clock.items()}
        request = suggestions_pb2.SuggestionsRequest(
            orderID=order_id,
            title=title,
            author=author,
            vector_clock=suggestions_pb2.VectorClock(entries=vector_clock_entries)
        )
        response = stub.BookSuggestions(request)
        # Convert the vector clock back to a dictionary
        updated_vector_clock = {key: value for key, value in response.vector_clock.entries.items()}
        # Return the list of suggested titles and the updated vector clock
        return response.titles, updated_vector_clock


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

    """
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
    """

    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = []

        # Start with transaction verification
        future_tv = executor.submit(
            verify_transaction,
            request_data,
            order_id,
            vector_clock
        )
        futures.append(future_tv)

        # Wait for transaction verification to complete before proceeding
        for future in as_completed(futures):
            is_valid, message, updated_vc = future.result()
            if not is_valid:
                order_status = 'Order Rejected'
                break  # Exit the loop early if transaction is not valid
            vector_clock = update_vector_clock(vector_clock, updated_vc)
            futures = []  # Reset futures list for the next set of tasks

            # Proceed with fraud detection for user data
            future_fd_user = executor.submit(
                detect_fraud,
                request_data['user'],
                request_data.get('creditCard', {}),
                order_id,
                vector_clock
            )
            futures.append(future_fd_user)

            # Wait for user data fraud check to complete
            for future in as_completed(futures):
                is_fraud, reason, updated_vc = future.result()
                if is_fraud:
                    order_status = 'Order Rejected'
                    break  # Exit the loop early if fraud is detected
                vector_clock = update_vector_clock(vector_clock, updated_vc)
                futures = []  # Reset futures list for the next set of tasks

                # Now verify credit card format and check for fraud
                future_cc_format = executor.submit(
                    verify_credit_card_format,
                    request_data['creditCard'],
                    order_id,
                    vector_clock
                )
                future_fd_cc = executor.submit(
                    check_credit_card_for_fraud,
                    request_data['creditCard'],
                    order_id,
                    vector_clock
                )
                futures.extend([future_cc_format, future_fd_cc])

                # Wait for both to complete
                for future in as_completed(futures):
                    result = future.result()
                    if not result[0]:
                        order_status = 'Order Rejected'
                        break  # Exit the loop early if any check fails
                    vector_clock = update_vector_clock(vector_clock, result[2])

                if order_status == 'Order Rejected':
                    break  # Exit the outer loop if order is rejected

                # Finally, generate book suggestions
                titles, updated_vc = generate_book_suggestions(
                    request_data['items'][0]['name'],  # Assuming there's at least one item
                    order_id,
                    vector_clock
                )
                vector_clock = update_vector_clock(vector_clock, updated_vc)
                suggested_books = titles
                order_status = 'Order Approved'

    # Construct the response
    response = {
        'orderId': order_id,
        'status': order_status,
        'suggestedBooks': suggested_books if order_status == 'Order Approved' else []
    }
    return jsonify(response)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
