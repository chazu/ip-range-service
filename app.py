from flask import Flask
import json
from ipaddress import IPv4Network, IPv4Address

class Service:
    def __init__(self):
        self.subnets = []
        self.range = IPv4Network("10.0.0.0/8")

    def add_range(self, cidr):
        network = IPv4Network(cidr)
        self.subnets.append(network)

    def next_range(self, size):
        all_subnets = []
        for subnet in self.range.subnets(new_prefix=size):
            all_subnets.append(subnet)
        for subnet in self.subnets:
            all_subnets = [x for x in all_subnets if not x.overlaps(subnet)]
        if not all_subnets:
            raise Exception("No available subnets of the desired size")
        desired_subnet = all_subnets[0]
        self.subnets.append(desired_subnet)
        return desired_subnet




service = Service()

service.add_range("10.0.0.0/16")
service.add_range("10.1.0.0/16")
service.add_range("10.4.0.0/16")

app = Flask(__name__)

def network_to_dict(network):
    hosts = list(network.hosts())

    return {
        "network_address": str(network.network_address),
        "prefix": network.prefixlen,
        "lowest_ip": str(hosts[0]),
        "highest_ip": str(hosts[-1])
    }


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/subnets")
def list_subnets():
    results = [ network_to_dict(x) for x in service.subnets ]
    return json.dumps(results)
