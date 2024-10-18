# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /mi_task

# Copy only the requirements file to leverage Docker cache
COPY app/requirements.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Expose the port that the FastAPI app will be running on
EXPOSE 8000

# Set the command to run the FastAPI app when the container starts
CMD ["python", "main.py"]