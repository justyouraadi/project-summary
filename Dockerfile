FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apts/lists/*

WORKDIR /app

COPY requirements.txt /app
COPY app.py /app
COPY socket_events.py /app
COPY ai_service.py /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3046

CMD ["gunicorn","-w","4","-b","0.0.0.0:3046","app:app"]