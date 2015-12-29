import re
import urllib2
from unittest import TestCase

import web_server
from digitalocean_connector import DigitalOceanConnector


# running this test suite might charge some costs to your digitalocean account

class TestWebServer(TestCase):
    def test_whenRequestedActionStart_thenServerStarts(self):
        server = web_server.HttpServer(DigitalOceanConnector())
        response = urllib2.urlopen("http://127.0.0.1:8082", '{"target" : "dropletname", "action" : "start"}')
        self.assertTrue(re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$").match(response.read().decode()))
        server.stop()

    def test_whenRequestedActionStop_thenServerStops(self):
        server = web_server.HttpServer(DigitalOceanConnector())
        response = urllib2.urlopen("http://127.0.0.1:8082", '{"target" : "dropletname", "action" : "stop"}')
        self.assertTrue(response.read().decode(), 'deleted')
        server.stop()

    def test_whenMissingTarget_thenErrorReturned(self):
        server = web_server.HttpServer(DigitalOceanConnector())
        response = urllib2.urlopen("http://127.0.0.1:8082", '{"action" : "stop"}')
        server.stop()
        self.assertEquals(response.read().decode(), 'bad request, missing target')

    def test_whenMissingAction_thenErrorReturned(self):
        server = web_server.HttpServer(DigitalOceanConnector())
        response = urllib2.urlopen("http://127.0.0.1:8082", '{"target" : "dropletName"}')
        server.stop()
        self.assertEquals(response.read().decode(), 'bad request, missing action')

    def test_whenInvalidRequest_thenErrorReturned(self):
        server = web_server.HttpServer(DigitalOceanConnector())
        response = urllib2.urlopen("http://127.0.0.1:8082", 'foo')
        server.stop()
        self.assertEquals(response.read().decode(), 'Invalid request')
