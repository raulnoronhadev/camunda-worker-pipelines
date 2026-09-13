FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
      rclone gettext-base \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY services/service1/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/service1/ .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "-u", "worker.py"]