#!/usr/bin/env python
import logging
import os
import signal
import ssl
import sys
import json
import base64
import tornado.httpserver
import tornado.websocket

from tornado.options import define, options, parse_command_line

from port_forwarder import PortForwarder
from websocket_handler import ControlWebSocketHandler, SignallingWebSocketHandler, LocalSignallingWebSocketHandler
from auth_handlers import LoginHandler, LogoutHandler
from request_handlers import ProtectedHandler, NoAuthHandler, ConfigurationRequestHandler
from turn_server_manager import TurnServerManager
from display_manager import wake_up_display

# Current dir
dirname = os.path.dirname(__file__)

# Get private key and self-signed certificate
ssl_stuff_dir = os.path.join(dirname, "ssl_stuff")
ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain(os.path.join(ssl_stuff_dir, "startssl.crt"),
                        os.path.join(ssl_stuff_dir, "startssl.key"))

# Load OAuth2 settings in google_oauth2_settings
with open(os.path.join(dirname, "robot-pi-google-oauth2.json")) as json_data:
    google_oauth2_settings = json.load(json_data)

with open(os.path.join(dirname, "rolesdb.json")) as json_data:
    roles_settings = json.load(json_data)

# Settings
settings = dict(
    compress_response=True,
    cookie_secret=base64.b64encode(os.urandom(50)).decode("ascii"),
    login_url="/auth",
    debug=True,
    xsrf_cookies=True,
    google_oauth=dict(
        key=google_oauth2_settings["web"]["client_id"],
        secret=google_oauth2_settings["web"]["client_secret"]
    ),
    roles=roles_settings
)

# Application routes
handlers = [
    (r"/auth", LoginHandler),
    (r"/logout", LogoutHandler),
    (r"/controller/(.*)", ProtectedHandler),
    (r"/robot/(.*)", NoAuthHandler),
    (r"/websocket_control", ControlWebSocketHandler),
    (r"/websocket_robot_signaling", LocalSignallingWebSocketHandler),
    (r"/websocket_controller_signaling", SignallingWebSocketHandler),
    (r"/turn_configuration", ConfigurationRequestHandler)
]

app = tornado.web.Application(
    handlers,
    **settings)

turn_server = None
port_forwarder = None
hostname = "robot-pi.bclouet.eu"


def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    log.info("Shutting down application")
    log.debug("Disabling port forwarding")
    turn_server.stop_turn_server()
    port_forwarder.disable_port_forwarding()
    log.debug("Stopping Tornado server")
    tornado.ioloop.IOLoop.instance().stop()
    log.info("Application stopped")
    sys.exit(0)

# Create a secure http listener
ssl_http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)
upstream_http_server = tornado.httpserver.HTTPServer(app)

if __name__ == '__main__':
    parse_command_line()
    set_exit_handler(on_exit)
    logging.getLogger("tornado.web").setLevel(logging.DEBUG)
    log = logging.getLogger("tornado.application")
    log.setLevel(logging.DEBUG)
    upstream_http_server.listen(8888)
    ssl_http_server.listen(8443, "127.0.0.1")
    log.debug("Enabling port forwarding")
    port_forwarder = PortForwarder()
    port_forwarder.enable_port_forwarding()
    port_forwarder.setup_external_ip(hostname=hostname)
    internal_ip, external_ip = port_forwarder.get_network_adresses()
    turn_server = TurnServerManager(cert=os.path.join(ssl_stuff_dir, "startssl.crt"),
                                    key=os.path.join(ssl_stuff_dir, "startssl.key"),
                                    internal_ip=internal_ip,
                                    external_ip=external_ip,
                                    realm=hostname,
                                    secret=base64.b64encode(os.urandom(50)).decode('ascii'),
                                    other_options="--lt-cred-mech --fingerprint --pidfile /tmp/turnserver.pid")
    turn_server.start_turn_server()
    log.info("Starting Tornado server")
    tornado.ioloop.PeriodicCallback(wake_up_display, 1000 * 60 * 5).start()
    tornado.ioloop.IOLoop.instance().start()