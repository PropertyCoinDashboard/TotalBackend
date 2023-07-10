FROM python:3.11
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /backend_pre/

RUN apt-get update && apt-get -y install libpq-dev
# RUN apt-get install -y netcat

COPY apps/apis/coin/coin_api_injection/data/bithum.csv apps/apis/coin/coin_api_injection/data/bithum.csv
COPY apps/apis/coin/coin_api_injection/data/korbit.csv apps/apis/coin/coin_api_injection/data/korbit.csv


COPY entrypoint.sh /usr/src/local/entrypoint.sh
COPY requirements/common.txt /backend_pre/
RUN pip install --upgrade pip
RUN pip install -r common.txt
COPY . /backend_pre/

RUN ["chmod", "+x", "/usr/src/local/entrypoint.sh"]



