
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend/

RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get install -y netcat

COPY requirements/common.txt /backend/
RUN pip install --upgrade pip
RUN pip install -r common.txt
COPY . /backend/