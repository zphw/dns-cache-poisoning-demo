FROM python:3.7

RUN apt-get update && apt-get install curl gnupg dnsutils iputils-ping net-tools -y

RUN pip3 install dnslib gevent

WORKDIR /src

COPY . .

ENTRYPOINT python dns.py