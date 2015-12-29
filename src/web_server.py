import json
import logging
import threading
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urllib2 import HTTPError

from digitalocean_connector import DigitalOceanConnector
from time_orchestrator import TimeOrchestrator

PORT_NUMBER = 8082


class HttpServer:
    def __init__(self, agent):
        self.server = HTTPServer(('127.0.0.1', PORT_NUMBER), RequestHandler)
        self.server.agent = agent
        logging.info('Listening ', PORT_NUMBER)
        threading.Thread(target=self.server.serve_forever).start()

    def stop(self):
        self.server.shutdown()
        self.server.socket.close()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
            if 'target' not in data:
                self.wfile.write("bad request, missing target")
                return
            if 'action' not in data:
                self.wfile.write("bad request, missing action")
                return

            if data['action'] == 'start':
                logging.info('serving start request')
                self.wfile.write(self.server.agent.start(data['target']))
            elif data['action'] == 'stop':
                logging.info('serving stop request')
                self.wfile.write(self.server.agent.stop(data['target']))
            else:
                logging.warn('unknown action ' + data['action'])
        except ValueError:
            logging.warn('invalid request')
            self.wfile.write("Invalid request")
        except HTTPError as e:
            logging.warn('request failed ' + e.msg)
            self.wfile.write("request failed")
        except Exception as e:
            logging.error('something went wrong ' + e.message)
            self.wfile.write("something went wrong")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='/var/log/digitalOceanBot.log', filemode='a')
    HttpServer(TimeOrchestrator(DigitalOceanConnector()))
