# Use the official Python 3.12.3 base image
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file to the working directory
# COPY pyproject.toml ./
COPY requirements.txt .

# Install the Python dependencies
RUN pip install -r requirements.txt 

# Copy the application code to the working directory
COPY . .

# Expose the port on which the application will run
EXPOSE 8000

# Run the FastAPI application using uvicorn
CMD ["python3", "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]