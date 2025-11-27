import grpc
import time
import concurrent.futures
import processor_pb2
import processor_pb2_grpc
import os

# Define max message size (256 MB)
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024
OPTIONS = [
    ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
    ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
]

def get_grpc_result(server_address, description, text_data):
    """
    Worker function to run in a separate PROCESS.
    """
    with grpc.insecure_channel(server_address, options=OPTIONS) as channel:
        stub = processor_pb2_grpc.TextProcessorStub(channel)
        request = processor_pb2.TextRequest(text=text_data)
        
        # Make the RPC call
        response = stub.Process(request)
        
        return {
            "description": description,
            "result": response.result,
            "time": response.time_taken
        }

def main():
    filename = "input_100mb.txt"
    try:
        with open(filename, "r") as f:
            TEXT = f.read()
    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return

    start_overall = time.time()

    # Define our targets
    servers = [
        ("wc_server:8001", "Word Count"),
        ("sent_server:8002", "Sentence Count"),
        ("max_server:8003", "Longest Word"),
        ("min_server:8004", "Shortest Word")
    ]

    results = []
    
    # ProcessPoolExecutor creates true OS processes
    with concurrent.futures.ProcessPoolExecutor(max_workers=4) as executor:
        future_to_server = {
            executor.submit(get_grpc_result, addr, desc, TEXT): desc 
            for addr, desc in servers
        }
        
        for future in concurrent.futures.as_completed(future_to_server):
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print(f"Task generated an exception: {exc}")

    end_overall = time.time()

    # --- FORMATTING OUTPUT TO MATCH IMAGE ---
    
    # Sort results to ensure the order matches the screenshot
    order_map = {
        "Word Count": 1,
        "Sentence Count": 2,
        "Longest Word": 3,
        "Shortest Word": 4
    }
    results.sort(key=lambda x: order_map.get(x['description'], 99))

    print("\n===== RESULTS =====")
    for res in results:
        # Format: Description: Result   (Time: X.XXXXXX sec)
        print(f"{res['description']}: {res['result']}   (Time: {res['time']:.6f} sec)")
    
    print("\n===== OVERALL EXECUTION TIME =====")
    print(f"{end_overall - start_overall:.6f} seconds\n")

if __name__ == "__main__":
    main()