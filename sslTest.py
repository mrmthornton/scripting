#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      IEUser
#
# Created:     26/04/2015
# Copyright:   (c) IEUser 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import socket
import ssl

print ssl.OPENSSL_VERSION

#ctx = OpenSSL.SSL.Context(OpenSSL.SSL.SSLv23_METHOD)
#ssock = OpenSSL.SSL.Connection(ctx, sock)
ctx = ssl.PROTOCOL_SSLv2
sock = socket.socket()
ssock = ssl.SSLSocket(sock)
print ssock.connect_ex(('www.ssllabs.com', 443))
#0
print ssock.send('GET /ssltest/viewMyClient.html HTTP/1.1\r\nHost: www.ssllabs.com\r\n\r\n')
#66
print ssock.recv(16384)
# HTTP -> chunked
print ssock.recv(16384)
print ssock.recv(16384)
#'2000\r\n'
d = ssock.recv(16384)
print d

print d.find('TLS 1.1')
#2324
print d.find('TLS 1.0')
#2432
d[2324:2432]

#def main():
#    pass

#if __name__ == '__main__':
#    main()
