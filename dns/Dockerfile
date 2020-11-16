FROM python:3.7

RUN pip3 install dnslib gevent

WORKDIR /src

COPY . .

ENTRYPOINT python server.py