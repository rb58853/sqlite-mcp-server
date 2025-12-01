FROM python:3.13-slim

# Set working directory
WORKDIR /

# Copy the rest of the application code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create sample database
RUN python3 database/create_sample_db.py

# Expose port
EXPOSE 8080

# Run the app
CMD ["python3", "main.py", "--host", "0.0.0.0", "--port", "8080"]