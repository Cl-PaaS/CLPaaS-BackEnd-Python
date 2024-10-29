FROM --platform=linux/amd64 python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["gunicorn", "--log-level", "info", "-b", "0.0.0.0:5000", "-w", "1", "app:app"]