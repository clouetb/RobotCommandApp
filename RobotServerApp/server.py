#!/usr/bin/env python
import logging
import os
import signal
import ssl
import sys
import json
import tornado.httpserver
import tornado.websocket

from tornado.web import RedirectHandler
from tornado.options import define, options, parse_command_line

from port_forwarder import enable_port_forwarding, disable_port_forwarding
from websocket_handler import WebSocketHandler
from login_handler import GoogleOAuth2LoginHandler
from file_handler import CustomStaticFileHandler

# Current dir
dirname = os.path.dirname(__file__)

# Listen on given port
define("port", default=8888, help="run on the given port", type=int)

port_forwarding = None

# Get private key and self-signed certificate
ssl_stuff_dir = os.path.join(dirname, "ssl_stuff")
ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain(os.path.join(ssl_stuff_dir, "startssl.crt"),
                        os.path.join(ssl_stuff_dir, "startssl.key"))

# Load OAuth2 settings in google_oauth2_settings
with open(os.path.join(dirname, "robot-pi-google-oauth2.json")) as json_data:
    google_oauth2_settings = json.load(json_data)

# Settings
settings = dict(
    cookie_secret=google_oauth2_settings["cookie_secret"],
    login_url="/auth",
    debug=True,
    xsrf_cookies=True,
    google_oauth=dict(
        key=google_oauth2_settings["web"]["client_id"],
        secret=google_oauth2_settings["web"]["client_secret"]
    )
)

# Application routes
handlers = [
    (r"/auth", GoogleOAuth2LoginHandler),
    (r"/(.*)", CustomStaticFileHandler, {"path": os.path.join(dirname, "templates")}),
    (r"/", RedirectHandler, {"url": "/index.html"}),
    (r"/websocket", WebSocketHandler)
]

app = tornado.web.Application(
    handlers,
    **settings)


def set_exit_handler(func):
    signal.signal(signal.SIGTERM, func)


def on_exit(sig, func=None):
    log.info("Shutting down application")
    log.debug("Disabling port forwarding")
    disable_port_forwarding(port_forwarding)
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
    enable_port_forwarding(port_forwarding)
    log.info("Starting Tornado server")
    tornado.ioloop.IOLoop.instance().start()