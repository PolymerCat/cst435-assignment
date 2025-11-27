import grpc
import time # Added for client time tracking
import text_analyzer_pb2 as pb2
import text_analyzer_pb2_grpc as pb2_grpc
import os
import sys

# --- Configuration ---
SERVER_ADDRESS = 'localhost:50051'
INPUT_FILE = 'input.txt'
# --- End Configuration ---

def check_stubs_are_ready():
    """
    Checks if the necessary gRPC stubs have been generated correctly.
    """
    try:
        # Check for the existence of the specific stub class
        if not hasattr(pb2_grpc, 'TextAnalyzerStub'):
            print("\n[SETUP ERROR]: The required 'TextAnalyzerStub' was not found in 'text_analyzer_pb2_grpc'.")
            print("This usually means the gRPC Python stubs have not been generated.")
            print("Please run the following command in this directory:")
            print("python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. text_analyzer.proto")
            sys.exit(1)
        return True
    except Exception as e:
        # Catch errors if the import failed entirely (less likely given the user's report)
        print(f"\n[SETUP ERROR]: Failed during stub check: {e}")
        sys.exit(1)


def run_client():
    """
    Reads a text file, connects to the gRPC server, and sends the content for analysis.
    """
    if not os.path.exists(INPUT_FILE):
        print(f"Error: Input file '{INPUT_FILE}' not found. Please create it.")
        return

    try:
        # Read the entire text content from the file
        with open(INPUT_FILE, 'r', encoding='utf-8') as f:
            text_to_analyze = f.read()

        if not text_to_analyze.strip():
            print("Error: Input file is empty.")
            return

        # Setup gRPC channel
        print(f"Connecting to Text Analyzer Server at {SERVER_ADDRESS}...")
        with grpc.insecure_channel(SERVER_ADDRESS) as channel:
            stub = pb2_grpc.TextAnalyzerStub(channel)

            # Create the request message
            request = pb2.AnalysisRequest(text_content=text_to_analyze)

            # Start client timer before the RPC call
            start_client_time = time.time()
            
            # Call the RPC
            print("Sending text for analysis...")
            response = stub.AnalyzeText(request)
            
            # Stop client timer after response is received
            end_client_time = time.time()
            total_client_time = end_client_time - start_client_time

            # Display results
            print("\n--- Analysis Results ---")
            print(f"Total Words: {response.word_count}")
            print(f"Total Sentences: {response.sentence_count}")
            print(f"Longest Word: '{response.longest_word}' ({len(response.longest_word)} chars)")
            print(f"Shortest Word: '{response.shortest_word}' ({len(response.shortest_word)} chars)")
            print("------------------------")
            print(f"Server Processing Time (Analysis only): {response.server_processing_time:.6f} seconds")
            print(f"Total RPC Time (Client to Server & Back): {total_client_time:.6f} seconds")
            print("------------------------\n")

    except grpc.RpcError as e:
        print(f"\n[RPC Error]: Could not connect to the server or call the RPC.")
        print(f"Details: {e.details()}")
    except Exception as e:
        print(f"\n[Client Error]: An unexpected error occurred: {e}")

if __name__ == '__main__':
    check_stubs_are_ready()
    run_client()