#!/usr/bin/env python
import ssl
import tornado.web
import tornado.websocket
import tornado.httpserver
import json
import logging
import os
import signal
import miniupnpc
import sys
from tornado.options import define, options, parse_command_line

# Current dir
dirname = os.path.dirname(__file__)

# Listen on given port
define("port", default=8888, help="run on the given port", type=int)

multicastif = None
minissdpdsocket = None
discoverdelay = 200
localport = 0
port_forwarding = None

# Get private key and self-signed certificate
ssl_stuff_dir = os.path.join(dirname, "ssl_stuff")
ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain(os.path.join(ssl_stuff_dir, "server.crt"),
                        os.path.join(ssl_stuff_dir, "server.key"))


def enable_port_forwarding():
    global port_forwarding
    try:
        # Create UPnP client
        port_forwarding = miniupnpc.UPnP(multicastif, minissdpdsocket, discoverdelay, localport)
        # Discover internet gateway device
        log.info("Discovering : %s detected", port_forwarding.discover())
        # Select internet gateway
        port_forwarding.selectigd()
        # Enabling port forwarding
        log.info("Setting up HTTP port mapping : %s", port_forwarding.addportmapping(8888, "TCP",
                                                                                     port_forwarding.lanaddr, 8888,
                                                                                     "Robot-Pi server listener", ""))
        log.info("Setting up TURN server port mapping : %s", port_forwarding.addportmapping(9999, "TCP",
                                                                                            port_forwarding.lanaddr,
                                                                                            9999,
                                                                                            "Turn server listener", ""))
    except Exception, e:
        log.error("Exception : %s", e)


def disable_port_forwarding():
    global port_forwarding
    try:
        log.info("Stopping HTTP port mapping : %s", port_forwarding.deleteportmapping(8888, "TCP"))
        log.info("Stopping TURN server port mapping : %s", port_forwarding.deleteportmapping(9999, "TCP"))
    except Exception, e:
        log.error("Exception : %s", e)


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def ping(self, value):
        log.debug("Received a ping responding")
        self.write_message("Pong")

    def set_speed(self, value):
        log.debug("Changing speed to L %s R %s", value[0], value[1])
        self.write_message("Setting speed to L %d R %d" % (value[0], value[1]))

    message_types = {
        "ping": ping,
        "speed": set_speed
    }

    # Needed for making secure websockets to work
    def check_origin(self, origin):
        return True

    def open(self, *args):
        self.stream.set_nodelay(True)

    def on_message(self, message):
        log.debug("Client received a message : %s", message)
        # Parse received json message
        actions = json.loads(message)
        # loop through messages payloads
        for k in actions.keys():
            # Call method with message verb
            self.message_types[k](self, actions[k])

    def on_close(self):
        pass


app = tornado.web.Application([
    (r'/socket', WebSocketHandler),
    # (r'/', IndexHandler),
    (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(dirname, "templates")})
], debug=True)


def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    log.info("Shutting down application")
    log.debug("Disabling port forwarding")
    disable_port_forwarding()
    log.debug("Stopping Tornado server")
    tornado.ioloop.IOLoop.instance().stop()
    log.info("Application stopped")
    sys.exit(0)

# Create a secure http listener
http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)

if __name__ == '__main__':
    parse_command_line()
    set_exit_handler(on_exit)
    log = logging.getLogger("tornado.application")
    log.setLevel(logging.DEBUG)
    http_server.listen(options.port)
    log.debug("Enabling port forwarding")
    enable_port_forwarding()
    log.info("Starting Tornado server")
    tornado.ioloop.IOLoop.instance().start()