import miniupnpc
import logging
import stun
import dns.resolver

log = logging.getLogger(__name__)
#log.setLevel(logging.DEBUG)

ports_mapping = [
    {
        "name": "Nginx HTTP frontend",
        "local_port": 443,
        "external_port": 443,
        "protocol": "TCP",
        "comment": "Nginx HTTP frontend",
        "target_addr": None
    },
    {
        "name": "Tornado HTTP frontend",
        "local_port": 8888,
        "external_port": 8888,
        "protocol": "TCP",
        "comment": "Robot-Pi server listener",
        "target_addr": None
    },
    {
        "name": "Signalmaster",
        "local_port": 9999,
        "external_port": 9999,
        "protocol": "TCP",
        "comment": "Signalmaster listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 3478,
        "external_port": 3478,
        "protocol": "TCP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 3479,
        "external_port": 3479,
        "protocol": "TCP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 5349,
        "external_port": 5349,
        "protocol": "TCP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 5350,
        "external_port": 5350,
        "protocol": "TCP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 3478,
        "external_port": 3478,
        "protocol": "UDP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 3479,
        "external_port": 3479,
        "protocol": "UDP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 5349,
        "external_port": 5349,
        "protocol": "UDP",
        "comment": "Turn server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 5350,
        "external_port": 5350,
        "protocol": "UDP",
        "comment": "Turn server listener",
        "target_addr": None
    }
]

multicastif = None
minissdpdsocket = None
discoverdelay = 200
localport = 0

#
port_forwarding = None


class PortForwarder:

    def __init__(self):
            # Create UPnP client
        self.upnpc = miniupnpc.UPnP(multicastif, minissdpdsocket, discoverdelay, localport)

    def enable_port_forwarding(self):
        try:
            # Discover internet gateway device
            log.debug("Discovering : %s detected", self.upnpc.discover())
            # Select internet gateway
            self.upnpc.selectigd()
            # Enabling port forwarding
            for port in ports_mapping:
                log.debug("About to setup %s: %s port mapping", port["name"], port)
                result = self.upnpc.addportmapping(port["local_port"],
                                               port["protocol"],
                                               port["target_addr"] or self.upnpc.lanaddr,
                                               port["external_port"],
                                               port["comment"], "")
                log.info("Setting up %s port mapping : %s %s -> %s:%s %s",
                         port["name"],
                         port["protocol"],
                         port["external_port"],
                         port["target_addr"] or self.upnpc.lanaddr,
                         port["local_port"],
                         result)
        except Exception, e:
            log.error("Exception : %s", e)

    def disable_port_forwarding(self):
        try:
            for port in ports_mapping:
                log.debug("About to delete %s: %s port mapping", port["name"], port)
                result = self.upnpc.deleteportmapping(port["external_port"],
                                               port["protocol"])
                log.info("Deleted %s port mapping : %s -> %s:%s %s", port["protocol"],
                         port["external_port"],
                         port["target_addr"] or self.upnpc.lanaddr,
                         port["local_port"],
                         result)
        except Exception, e:
            log.error("Exception : %s", e)

    def setup_external_ip(self, hostname=None):
        nat_type, current_external_ip, external_port = stun.get_ip_info()
        log.info("Nat type %s, external IP %s, external port %s", nat_type, current_external_ip, external_port)
        dns_registered_ip = dns.resolver.query(hostname)[0]
        if str(current_external_ip) != str(dns_registered_ip):
            log.info("DNS need change. Currently on DNS '%s', current external IP '%s'",
                     dns_registered_ip, current_external_ip)
        else:
            log.info("DNS and current external IP ('%s') are the same, no DNS change needed", current_external_ip)

    def get_network_adresses(self):
        """
        :return: (internal ip, external ip)
        """
        return self.upnpc.lanaddr, stun.get_ip_info()[1]

