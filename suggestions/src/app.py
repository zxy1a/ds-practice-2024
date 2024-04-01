import grpc
from concurrent import futures
import logging
import sys
import os

# This set of lines are needed to import the gRPC stubs.
# The path of the stubs is relative to the current file, or absolute inside the container.
# Change these lines only if strictly needed.
FILE = __file__ if '__file__' in globals() else os.getenv("PYTHONFILE", "")
utils_path = os.path.abspath(os.path.join(FILE, '../../../utils/pb/suggestions'))
sys.path.insert(0, utils_path)

from utils.vector_clock import VectorClock
from utils.pb.suggestions import suggestions_pb2, suggestions_pb2_grpc

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class SuggestionsServiceImpl(suggestions_pb2_grpc.SuggestionsServicer):
    def BookSuggestions(self, request, context):

        vc = VectorClock.from_proto(request.vector_clock)
        vc.increment("suggestions_service")

        logging.info(f"OrderID {request.orderID} - Current Vector Clock: {vc.get_clock()}")

        # Predefined list of book titles to suggest
        book_titles = [
            "The Great Gatsby",
            "To Kill a Mockingbird",
            "1984",
            "Pride and Prejudice",
            "The Catcher in the Rye"
        ]

        updated_vector_clock = vc.to_proto(suggestions_pb2.VectorClock)

         # Return response with updated vector clock
        return suggestions_pb2.SuggestionsResponse(
            titles=book_titles,
            vector_clock=updated_vector_clock 
        )


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    suggestions_pb2_grpc.add_SuggestionsServicer_to_server(
        SuggestionsServiceImpl(), server)
    server.add_insecure_port('[::]:50053')  # Use a different port if necessary
    server.start()
    logging.info("Suggestions Service running on port 50053")
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
