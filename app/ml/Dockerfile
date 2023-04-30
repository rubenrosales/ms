# Use the official Python image as the base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY . .

# Install the dependencies
RUN python setup.py sdist bdist_wheel

RUN pip install .