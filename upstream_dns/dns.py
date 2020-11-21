 # -*- coding: UTF-8 -*-

from dnslib import *
import gevent
from gevent.server import DatagramServer
from gevent import socket
from random import randint
from time import sleep

always_respond_ip = '1.2.3.4'

class DNSServer(DatagramServer):

    def handle_dns_request(self, data, address):

        req = DNSRecord.parse(data)
        qname = str(req.q.qname)
        qid = req.header.id

        response = DNSRecord(DNSHeader(qr=1, aa=1, ra=1),
                                     q=DNSQuestion(qname),
                                     a=RR(qname, rdata=A(always_respond_ip)))

        response.header.id = qid
        sleep(1.5)
        self.socket.sendto(response.pack(), address)
            

    def handle(self, data, address):

        self.handle_dns_request(data, address)


def main():
    DNSServer(':53').serve_forever()


if __name__ == '__main__':
    main()
