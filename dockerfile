# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required by LightGBM
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code
COPY . .

# Install the package in editable mode
RUN pip install --no-cache-dir -e .

# Accept Azure credentials as build args (passed from Jenkins, not baked in)
ARG AZURE_CONTAINER_NAME
ARG AZURE_BLOB_NAME
ARG AZURE_STORAGE_CONNECTION_STRING
ARG AZURE_CONNECTION_STRING_ENV=AZURE_STORAGE_CONNECTION_STRING
ENV AZURE_CONTAINER_NAME="$AZURE_CONTAINER_NAME"
ENV AZURE_BLOB_NAME="$AZURE_BLOB_NAME"
ENV AZURE_STORAGE_CONNECTION_STRING="$AZURE_STORAGE_CONNECTION_STRING"
ENV AZURE_CONNECTION_STRING_ENV="$AZURE_CONNECTION_STRING_ENV"

# Train the model before running the application
RUN python demo.py

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]