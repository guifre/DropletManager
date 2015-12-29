import json
import logging
import sys


class ConfigProvider:
    def parse(self):
        try:
            logging.debug('loading configuration')
            return json.loads(open("../resources/config.json", "r").read())
        except:
            print "Unexpected error:", sys.exc_info()[0]
            raise
