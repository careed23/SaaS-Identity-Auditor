# Use an official Python runtime as a parent image
# Slim version to reduce attack surface (Security Best Practice)
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# --no-cache-dir keeps the image small
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create a non-root user for security (Running as root is a vulnerability)
RUN useradd -m auditor_user
USER auditor_user

# Define the command to run the application
CMD ["python", "auditor.py"]