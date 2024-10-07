# Use the official Python image from Docker Hub
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt requirements.txt

# Install any necessary dependencies
RUN pip3 install -r requirements.txt

# Copy the rest of the application into the container
COPY . .

# Expose port 5000 to allow external connections to the Flask app
EXPOSE 5000

# Set environment variables (if needed, from .env file)
ENV FLASK_ENV=production

ARG MONGO_URI

ENV MONGO_URI=$MONGO_URI

# Command to run the Flask app
CMD ["python", "run.py"]