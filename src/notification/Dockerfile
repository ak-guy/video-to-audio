FROM python:3.10-slim-bullseye

RUN apt-get update

RUN apt-get install -y --no-install-recommends --no-install-suggests build-essential

WORKDIR /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir --requirement /app/requirements.txt
COPY . /app

CMD ["python3", "consumer.py"]
