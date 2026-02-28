FROM python:3.11

RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3046

CMD ["gunicorn", "-k", "eventlet", "-w", "1", "-b", "0.0.0.0:3046", "app:app"]
