import logging
from threading import Timer

TIME_TO_STOP_DROPLET = 3480.0  # 58 minutes in seconds


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
            Timer(TIME_TO_STOP_DROPLET, self.stop_droplet, [target], {}).start()
            logging.info("starting and scheduled stop process")
            self.droplet_ip = self.digital_ocean_connector.start(target)
        return self.droplet_ip

    def stop(self, target):
        logging.info("stop request received")
        self.stop_requested = True
        return 'deletion scheduled'

    def stop_droplet(self, target):
        logging.info(
            "running stop, stop requested is " + str(self.stop_requested) + " and started " + str(self.started))
        if self.stop_requested and self.started:
            logging.info("stopping")
            self.digital_ocean_connector.stop(target)
            self.started = False
