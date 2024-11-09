# Use the official Python image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Run Gunicorn
CMD ["fastapi", "run", "main.py", "--port", "8084"]