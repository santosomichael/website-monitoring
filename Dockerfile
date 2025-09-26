# File: Dockerfile
# Use the official Playwright image that includes Python
FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

WORKDIR /app
COPY requirements.txt .
# Install the Python dependencies
RUN pip install -r requirements.txt

COPY . .
# The command to run the Python script
CMD ["python", "app.py"]