
FROM python:3.11-slim

# Set our working directory inside the container
WORKDIR /app

# Copy the shopping list and install the MCP and HTTPX libraries
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our Python gateway script
COPY server.py .

# SRE Trick: Keep the container alive indefinitely in the background. 
# This allows the AI client to connect and execute the script on-demand via 'docker exec'.
CMD ["sleep", "infinity"]