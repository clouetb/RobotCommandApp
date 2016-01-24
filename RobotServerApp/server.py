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

from port_forwarder import enable_port_forwarding, disable_port_forwarding, setup_external_ip
from websocket_handler import ControlWebSocketHandler, SignallingWebSocketHandler, LocalSignallingWebSocketHandler
from auth_handlers import LoginHandler, LogoutHandler
from request_handlers import ProtectedHandler, NoAuthHandler

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
    cookie_secret=base64.b64encode(os.urandom(50)).decode('ascii'),
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
    (r"/websocket_controller_signaling", SignallingWebSocketHandler)
]

app = tornado.web.Application(
    handlers,
    **settings)


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
    enable_port_forwarding()
    setup_external_ip()
    log.info("Starting Tornado server")
    tornado.ioloop.IOLoop.instance().start()