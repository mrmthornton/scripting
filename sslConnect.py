#-------------------------------------------------------------------------------
# Name:        sslConnect.py
# Purpose:     test for
#
# Author:      IEUser
#
# Created:     01/07/2015
# Copyright:   (c) IEUser 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import requests
from requests
import httplib

conn = httplib.HTTPConnection("www.python.org")
conn.request("GET", "/index.html")
#conn = httplib.HTTPSConnection("www.python.org")
#conn.request("CONNECT", "/index.html")

r1 = conn.getresponse()
print r1.status, r1.reason

