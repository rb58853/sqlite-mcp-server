FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure runtime directories exist
RUN mkdir -p /app/database/data /app/log

# Expose port
EXPOSE 8080

# Create the sample DB at container startup (if missing) and run the API
CMD ["sh", "-c", "python3 database/create_sample_db.py --if-missing && python3 main.py --host 0.0.0.0 --port 8080"]