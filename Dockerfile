# Base image with Python installed
FROM python:3.11

# Set working directory inside container
WORKDIR /app

# Copy requirements first to leverage Docker layer caching
COPY app/requirements.txt .
RUN pip install -r requirements.txt

# Copy the application code
COPY app .

# Start the FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]