FROM python:3.10

WORKDIR /app

# Install gRPC dependencies
RUN pip install grpcio grpcio-tools

COPY . .

# Generate the gRPC Python code from the proto file
# This assumes processor.proto is in the same directory
RUN python3 -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. processor.proto

CMD ["python3", "client.py"]