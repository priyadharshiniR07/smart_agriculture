# Dockerfile

FROM python:3.9-slim

WORKDIR /app

COPY smart_agriculture/ /app/

RUN pip install flask

EXPOSE 5000

CMD ["python", "app.py"]
