FROM python:3.7

RUN pip install scapy

RUN apt-get update && apt-get install curl gnupg dnsutils iputils-ping net-tools -y

WORKDIR /src

COPY . .

ENTRYPOINT /bin/bash
