FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip uninstall -y pip \
    && adduser -D -H -u 10001 app

COPY app ./app

USER 10001

EXPOSE 5001

CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "2", "--worker-tmp-dir", "/dev/shm", "--no-control-socket", "app.app:app"]
