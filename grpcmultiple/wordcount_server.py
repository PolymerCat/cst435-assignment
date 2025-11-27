import time
import grpc
from concurrent import futures
import processor_pb2
import processor_pb2_grpc

# 256 MB max message size
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024

class WordCount(processor_pb2_grpc.TextProcessorServicer):
    def Process(self, request, context):
        start = time.time()
        # Logic: Count words
        if not request.text:
            count = 0
        else:
            count = len(request.text.split())
        end = time.time()
        return processor_pb2.TextResponse(result=str(count), time_taken=end - start)

def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        options=[
            ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
            ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH),
        ]
    )
    processor_pb2_grpc.add_TextProcessorServicer_to_server(WordCount(), server)
    server.add_insecure_port('[::]:8001')
    print("Wordcount (gRPC) Server running on port 8001...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()