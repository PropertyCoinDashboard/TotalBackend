FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend/

RUN apt-get update && apt-get -y install libpq-dev
RUN apt-get install -y netcat

COPY data/bithum.csv /backend/api_injection/data/bithum.csv
COPY data/korbit.csv /backend/api_injection/data/korbit.csv

COPY entrypoint.sh /usr/src/local/entrypoint.sh
COPY requirements/common.txt /backend/
RUN pip install --upgrade pip
RUN pip install -r common.txt
COPY . /backend/

RUN ["chmod", "+x", "/usr/src/local/entrypoint.sh"]



