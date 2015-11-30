#!/usr/bin/env python
import ssl
import tornado.web
import tornado.websocket
import tornado.httpserver
import json
import logging
import os
import sys

from tornado.options import define, options, parse_command_line

dirname = os.path.dirname(__file__)
define("port", default=8888, help="run on the given port", type=int)
ssl_stuff_dir = os.path.join(dirname, "ssl_stuff")

ssl_ctx = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_ctx.load_cert_chain(os.path.join(ssl_stuff_dir, "server.crt"),
                        os.path.join(ssl_stuff_dir, "server.key"))


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

    def check_origin(self, origin):
        return True

    def open(self, *args):
        self.stream.set_nodelay(True)

    def on_message(self, message):
        log.debug("Client received a message : %s", message)
        actions = json.loads(message)
        for k in actions.keys():
            self.message_types[k](self, actions[k])

    def on_close(self):
        pass


app = tornado.web.Application([
        (r'/socket', WebSocketHandler),
        #(r'/', IndexHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(dirname,"templates")})
    ], debug=True)
http_server = tornado.httpserver.HTTPServer(app, ssl_options=ssl_ctx)


if __name__ == '__main__':
    try:
        parse_command_line()
        log = logging.getLogger("tornado.application")
        log.setLevel(logging.DEBUG)
        http_server.listen(options.port)
        log.debug("Starting Tornado server")
        tornado.ioloop.IOLoop.instance().start()
    except KeyboardInterrupt:
        log.info("Shutting down application")
        log.debug("Stopping Tornado server")
        tornado.ioloop.IOLoop.instance().stop()
        log.info("Application stopped")
        sys.exit(0)
