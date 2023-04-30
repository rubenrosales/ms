# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY api/ .

# Expose port 5000 to the host machine
EXPOSE 5000

# Set the command to run when the container starts
CMD ["python", "flask-app.py"]
