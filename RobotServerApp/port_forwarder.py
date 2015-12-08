import miniupnpc
import logging


log = logging.getLogger(__name__)


ports_mapping = [
    {
        "name": "HTTP",
        "local_port": 8888,
        "external_port": 8888,
        "protocol": "TCP",
        "comment": "Robot-Pi server listener",
        "target_addr": None
    },
    {
        "name": "TURN",
        "local_port": 9999,
        "external_port": 9999,
        "protocol": "TCP",
        "comment": "Turn server listener",
        "target_addr": None
    }

]


multicastif = None
minissdpdsocket = None
discoverdelay = 200
localport = 0


def enable_port_forwarding(port_forwarding):
    try:
        # Create UPnP client
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


def disable_port_forwarding(port_forwarding):
    try:
        for port in ports_mapping:
            log.debug("About to delete %s: %s port mapping", port["name"], port)
            result = port_forwarding.deleteportmapping(port["external_port"],
                                           port["protocol"])
            log.info("Deleted %s port mapping : %s %s -> %s:%s %s", port["protocol"],
                     port["external_port"],
                     port["target_addr"] or port_forwarding.lanaddr,
                     port["local_port"],
                     result)
    except Exception, e:
        log.error("Exception : %s", e)