FROM ubuntu:latest

RUN apt-get update && apt-get install curl gnupg dnsutils iputils-ping net-tools -y

ENTRYPOINT echo nameserver 10.0.0.2 > /etc/resolv.conf && /bin/bash
