# Base image with Python
FROM python:3.12

# Set working directory
WORKDIR /app

# Install required Python package
RUN pip install huggingface_hub

# Copy the Python script into the container
COPY download_adapters.py /app/download_adapters.py

# Set default command
CMD ["python", "/app/download_adapters.py"]
