FROM python:3.5-alpine3.8

EXPOSE 9090

RUN mkdir -p /app/mocksi

COPY mocksi/ /app/mocksi
COPY config.yaml /app/config.yaml
COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt

ENV PYTHONPATH "$PYTHONPATH:/app"
ENV MOCKSI_CONFIG_FILE /app/config.yaml

WORKDIR /app

CMD ["python", "mocksi/mocksi_server.py"]
