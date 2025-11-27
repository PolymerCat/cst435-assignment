import grpc
import time
from concurrent import futures

# Import generated gRPC files (will be generated from .proto)
import text_analyzer_pb2 as pb2
import text_analyzer_pb2_grpc as pb2_grpc

# Import local analysis functions
from analysis_functions import get_analysis_results

class TextAnalyzerServicer(pb2_grpc.TextAnalyzerServicer):
    """Implements the TextAnalyzer service defined in the proto file."""

    def AnalyzeText(self, request, context):
        """
        Receives the text content and performs the required analysis.
        """
        print(f"Received request to analyze text (length: {len(request.text_content)} characters).")

        text_content = request.text_content

        # Get results and server time using the updated analysis module
        results, server_time = get_analysis_results(text_content)

        # Create and return the AnalysisResponse object
        response = pb2.AnalysisResponse(
            word_count=results['word_count'],
            sentence_count=results['sentence_count'],
            longest_word=results['longest_word'],
            shortest_word=results['shortest_word'],
            server_processing_time=server_time # NEW: Send server time
        )
        print(f"Analysis complete. Server time: {server_time:.6f}s. Sending response.")
        return response

def serve():
    """Starts the gRPC server with a larger message size limit."""
    # Set the max message size limit for incoming requests to 50MB (52428800 bytes)
    MAX_MESSAGE_LENGTH = 120 * 1024 * 1024

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ]
    )
    pb2_grpc.add_TextAnalyzerServicer_to_server(
        TextAnalyzerServicer(), server
    )
    # The server runs on port 50051
    server.add_insecure_port('[::]:50051')
    server.start()
    print(f"Text Analyzer Server started on port 50051 (Max message size: {MAX_MESSAGE_LENGTH / (1024*1024):.0f}MB). Awaiting client connections...")
    try:
        while True:
            time.sleep(86400) # One day
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()