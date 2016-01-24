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


def enable_port_forwarding():
    try:
        # Create UPnP client
        global port_forwarding
        port_forwarding = miniupnpc.UPnP(multicastif, minissdpdsocket, discoverdelay, localport)
        # Discover internet gateway device
        log.debug("Discovering : %s detected", port_forwarding.discover())
        # Select internet gateway
        port_forwarding.selectigd()
        # Enabling port forwarding
        for port in ports_mapping:
            log.debug("About to setup %s: %s port mapping", port["name"], port)
            result = port_forwarding.addportmapping(port["local_port"],
                                           port["protocol"],
                                           port["target_addr"] or port_forwarding.lanaddr,
                                           port["external_port"],
                                           port["comment"], "")
            log.info("Setting up %s port mapping : %s %s -> %s:%s %s",
                     port["name"],
                     port["protocol"],
                     port["external_port"],
                     port["target_addr"] or port_forwarding.lanaddr,
                     port["local_port"],
                     result)
    except Exception, e:
        log.error("Exception : %s", e)


def disable_port_forwarding():
    global port_forwarding
    try:
        for port in ports_mapping:
            log.debug("About to delete %s: %s port mapping", port["name"], port)
            result = port_forwarding.deleteportmapping(port["external_port"],
                                           port["protocol"])
            log.info("Deleted %s port mapping : %s -> %s:%s %s", port["protocol"],
                     port["external_port"],
                     port["target_addr"] or port_forwarding.lanaddr,
                     port["local_port"],
                     result)
    except Exception, e:
        log.error("Exception : %s", e)


def setup_external_ip():
    nat_type, current_external_ip, external_port = stun.get_ip_info()
    log.info("Nat type %s, external IP %s, external port %s", nat_type, current_external_ip, external_port)
    dns_registered_ip = dns.resolver.query("robot-pi.bclouet.eu")[0]
    if str(current_external_ip) != str(dns_registered_ip):
        log.info("DNS need change. Currently on DNS '%s', current external IP '%s'",
                 dns_registered_ip, current_external_ip)
    else:
        log.info("DNS and current external IP ('%s') are the same, no DNS change needed", current_external_ip)


def get_network_adresses(port_forwarding):
    return port_forwarding.lanaddr, stun.get_ip_info()[1]

