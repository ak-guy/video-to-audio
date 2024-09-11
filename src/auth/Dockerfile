FROM python:3.10-slim-bullseye

RUN apt-get update

RUN apt-get install -y --no-install-recommends --no-install-suggests default-libmysqlclient-dev build-essential pkg-config

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]
