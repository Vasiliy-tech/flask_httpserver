#!/usr/bin/env python

import re
import socket
import httplib
import unittest
import httplib, urllib
a=0
class HttpServer(unittest.TestCase):
  host = "localhost"
  port = 5000

  def setUp(self):
    self.conn = httplib.HTTPConnection(self.host, self.port, timeout=10)

  def tearDown(self):
    self.conn.close()

  # def test_server_header(self):
  #   # """Server header exists"""
  #   self.conn.request("GET", "/")
  #   r = self.conn.getresponse()
  #
  #   server = r.read()
  #
  #   if server == 'Hello World!':
  #       print('fsdfsd')
  #
  #   self.assertIsNotNone(server)


  def test_post_request(self):
    # params = urllib.urlencode({'key': 'mail.ru', 'value': 'target'})
    params = '{"key": "mail.ru", "value": "target"}'
    # headers = {"Content-type": "application/x-www-form-urlencoded",
    #          "Accept": "text/plain"}
    self.conn.request("POST", "/dictionary", params)
    response = self.conn.getresponse()



suite = unittest.TestSuite((
        unittest.makeSuite(HttpServer),
    ))

result = unittest.TextTestRunner().run(suite)
