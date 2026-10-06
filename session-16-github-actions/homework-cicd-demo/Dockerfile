FROM python:3.14-slim

ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION} \
    PORT=8000 \
    PYTHONUNBUFFERED=1

WORKDIR /srv
COPY app/ app/

USER 10001
EXPOSE 8000

HEALTHCHECK --interval=5s --timeout=3s --retries=5 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/healthz')"]

CMD ["python", "-m", "app.server"]
