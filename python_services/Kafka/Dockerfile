FROM python:3.9
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all async components
COPY *.py ./

ENV PYTHONPATH=/app

# Default command - can be overridden when running the container
CMD ["python", "-m","python_services.Kafka.consumer", "python_services.Kafka.response_consumer"]

