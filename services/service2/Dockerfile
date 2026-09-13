FROM python:3.12-slim

WORKDIR /app

COPY services/service2/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/service2/ .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
CMD ["python", "-u", "worker.py"]
