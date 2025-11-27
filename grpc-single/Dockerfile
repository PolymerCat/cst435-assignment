# Use a slim Python image for a smaller footprint
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the analysis logic, the proto file, and the server implementation
COPY text_analyzer.proto .
# Re-generate stubs because text_analyzer.proto was updated
RUN python -m grpc_tools.protoc -I. --python_out=. --pyi_out=. --grpc_python_out=. text_analyzer.proto
COPY analysis_functions.py .
COPY text_analyzer_server.py .

# Expose the gRPC port
EXPOSE 50051

# Command to run the server
CMD ["python", "text_analyzer_server.py"]