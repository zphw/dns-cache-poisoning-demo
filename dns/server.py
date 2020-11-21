 # -*- coding: UTF-8 -*-

import dnslib
import gevent
from gevent.server import DatagramServer
from gevent import socket
from random import randint

ns = '10.0.0.5'


class Cache:
    def __init__(self):
        self.list = {}

    def get(self, key):
        return self.list.get(key, None)

    def set(self, key, value):
        self.list[key] = value

cache = Cache()


class DNSServer(DatagramServer):

    def handle_dns_request(self, data, address):

        req = dnslib.DNSRecord.parse(data)
        qname = str(req.q.qname)
        qid = req.header.id

        record = cache.get(qname)

        if record:

            response = dnslib.DNSRecord.parse(record)
            response.header.id = qid
            self.socket.sendto(response.pack(), address)

        else:

            request = dnslib.DNSRecord.parse(data)
            qid_to_request = randint(10000, 10050)
            request.header.id = qid_to_request

            address = (ns, 53)
            sock = socket.socket(type=socket.SOCK_DGRAM)
            sock.bind(('10.0.0.2', 22222))
            sock.connect(address)
            sock.send(request.pack())

            dns_response, dns_address = sock.recvfrom(8192)
            response = dnslib.DNSRecord.parse(dns_response)

            while response.header.id != qid_to_request:
                dns_response, dns_address = sock.recvfrom(8192)
                response = dnslib.DNSRecord.parse(dns_response)

            if response.header.id == qid_to_request:
                qname = str(response.q.qname)
                cache.set(qname, dns_response)
                response.header.id = qid
                print(response)
                self.socket.sendto(response.pack(), address)
            

    def handle(self, data, address):

        self.handle_dns_request(data, address)


def main():
    DNSServer('10.0.0.2:53').serve_forever()


if __name__ == '__main__':
    main()
