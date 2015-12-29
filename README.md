# DropletManager

It is a simple microservice written in python. It exposes a JSON resource API through HTTP that facilitates restoring digital ocean droplets from snapshots and destroying them.

If you need to run a task or expose a service for a determined period of time, DropletManager might help you to reduce costs of you Digital Ocean bill.

You need to change the file **/resources/config** with your Digital Ocean API key. Once DropletManager is started, it will listen to loopback port 8082 for incomming HTTP requests.


* To create a new droplet from a snapshot, make a post request with the following body

```JSON
{"target" : "DROPLET_NAME", "action" : "start"}
``` 

* To destroy a existing droplet, make a post request with the following body

```JSON
 {"target" : "DROPLET_NAME", "action" : "stop"}
``` 


Hope it might be useful to someone.
