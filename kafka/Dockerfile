FROM python:3.9
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all async components
COPY producer.py consumer.py response_consumer.py config.py ./

# Default command - can be overridden when running the container
CMD ["python", "consumer.py"]
