import time
import grpc
from concurrent import futures
import processor_pb2
import processor_pb2_grpc

# 256 MB max message size
MAX_MESSAGE_LENGTH = 256 * 1024 * 1024

class SentenceCount(processor_pb2_grpc.TextProcessorServicer):
    def Process(self, request, context):
        start = time.time()
        # Logic: Count sentences based on punctuation
        count = request.text.count('.') + request.text.count('!') + request.text.count('?')
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
    processor_pb2_grpc.add_TextProcessorServicer_to_server(SentenceCount(), server)
    server.add_insecure_port('[::]:8002')
    print("Sentence (gRPC) Server running on port 8002...")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()