import json
import logging
import time
import urllib2

from config_provider import ConfigProvider


class DigitalOceanConnector:
    def __init__(self):
        self.config = ConfigProvider().parse()

    def start(self, target):
        if self.find_droplet(target) is None:
            image = self.find_image()
            if image is None:
                logging.error('image not found')
                return 'image not found'
            self.create(image)
            return self.wait_until_stated(target)

    def stop(self, target):
        droplet = self.find_droplet(target)
        if droplet is None:
            return 'dropled does not exist'

        logging.info('deleting ' + str(droplet['id']))
        return self.delete(droplet['id'])

    def delete(self, droplet_id):
        req = urllib2.Request('https://api.digitalocean.com/v2/droplets/' + str(droplet_id))
        req.add_header("Content-Type", "application/json")
        req.add_header('Authorization', 'Bearer ' + self.config['api_key'])
        req.get_method = lambda: 'DELETE'
        urllib2.urlopen(req)
        return 'deleted'

    def create(self, image_id):
        logging.info('creating droplet')
        data = '{' + \
               '"name" : "' + image_id['name'] + \
               '", "region" : "' + image_id['regions'][0] + \
               '", "size" : "' + self.config['size'] + \
               '", "image" : "' + str(image_id['id']) + \
               '", "ssh_keys" : ["' + self.find_keys() + '"]' + \
               ', "backups" : false' + \
               ', "ipv6" : false' + \
               ', "private_networking" : null' + \
               ', "user_data" : null' + '}'

        logging.debug('requesting ' + data)
        req = urllib2.Request('https://api.digitalocean.com/v2/droplets/', data)
        req.add_header('Authorization', 'Bearer ' + self.config['api_key'])
        req.add_header("Content-Type", "application/json")
        return urllib2.urlopen(req).read()

    def find_droplet(self, target):
        req = urllib2.Request('https://api.digitalocean.com/v2/droplets?page=1&per_page=100')
        req.add_header('Authorization', 'Bearer ' + self.config['api_key'])
        data = json.load(urllib2.urlopen(req))
        for droplet in data['droplets']:
            if droplet['name'] == target:
                return droplet
        return None

    def find_image(self):
        req = urllib2.Request('https://api.digitalocean.com/v2/images?page=1&per_page=100')
        req.add_header('Authorization', 'Bearer ' + self.config['api_key'])
        data = json.load(urllib2.urlopen(req))
        for image in data['images']:
            if image['name'] == self.config['snapshot'] and image['type'] == 'snapshot':
                logging.debug('found snapshot ' + str(image))
                return image
        return None

    def find_keys(self):
        req = urllib2.Request('https://api.digitalocean.com/v2/account/keys')
        req.add_header('Authorization', 'Bearer ' + self.config['api_key'])
        urlopen = urllib2.urlopen(req)
        data = json.load(urlopen)
        return str(data['ssh_keys'][0]['id'])  # todo allow more keys, guard against no keys etc

    def wait_until_stated(self, target):
        droplet = self.find_droplet(target)
        if 'status' not in droplet:
            return 'something went wrong ' + str(droplet)
        while 'new' == droplet['status']:
            logging.debug('still waiting')
            time.sleep(6)
            droplet = self.find_droplet(target)
        return str(droplet['networks']['v4'][0]['ip_address'])
