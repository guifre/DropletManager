import logging
from threading import Timer

TIME_TO_STOP_DROPLET = 3480  # 58 minutes in seconds


class TimeOrchestrator:
    def __init__(self, digital_ocean_connector):
        self.stop_requested = False
        self.started = False
        self.digital_ocean_connector = digital_ocean_connector

    def start(self, target):
        logging.info("start request received")
        if self.started is False:
            self.started = True
            self.stop_requested = False
            Timer(TIME_TO_STOP_DROPLET, self.stop_droplet, target)
            logging.info("starting and scheduled stop process")
            self.droplet_ip = self.digital_ocean_connector.start(target)
        return self.droplet_ip

    def stop(self, target):
        logging.info("stop request received")
        self.stop_requested = True
        return 'deletion scheduled'

    def stop_droplet(self, target):
        if self.stop_requested and self.started is True:
            self.digital_ocean_connector.stop(target)
            self.started = False
