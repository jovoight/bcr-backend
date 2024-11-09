# Use the official Python image
FROM python:3.13

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt requirements.txt

# Copy the application code
COPY . /app

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# SQLite DB volume
VOLUME /app/db

# Open port 8084
EXPOSE 8084

# Run the server 
CMD ["fastapi", "run", "main.py", "--port", "8084"]