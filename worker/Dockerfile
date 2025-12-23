FROM python:3.11-slim

# Keep everything under a single, consistent working directory so runtime paths are stable
WORKDIR /app/worker

# Install dependencies first for better build caching
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the worker source after installing dependencies
COPY . .

# Run the worker from the copied source location
CMD ["python", "main.py"]