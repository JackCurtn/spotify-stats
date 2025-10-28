FROM python:3.9-slim

WORKDIR /app

# Copy requirements.txt from the project root
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your app code from the app folder
COPY app/ .

EXPOSE 8050

CMD ["python", "app.py"]
