import json
import logging
import tornado.websocket

import display_manager

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class RootWebSocketHandler(tornado.websocket.WebSocketHandler):
    # Needed to fetch the authenticated user
    def get_current_user(self):
        return self.get_secure_cookie("user")

    # Overridden for dealing with authentication
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        log.debug("Incoming request %s", self.request)
        # Fail if not authenticated
        if not self.current_user:
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        log.debug("User is %s", self.get_current_user())
        # Continue websocket handshake
        super(RootWebSocketHandler, self).get(*args, **kwargs)

    # Needed for making secure cross-domain websockets to work
    def check_origin(self, origin):
        return True

    def open(self, *args):
        log.debug("Connection incoming")
        self.stream.set_nodelay(True)


class SignallingWebSocketHandler(tornado.websocket.WebSocketHandler):
    clients = []

    # Equality operators used for keeping the clients array tidy
    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and other.request.headers.get('X-Forwarded-For') == self.request.headers.get('X-Forwarded-For'))

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_local(self):
        if not ((str(self.request.headers.get('X-Forwarded-For')) == "127.0.0.1") or
                    (str(self.request.headers.get('X-Forwarded-For')) == "::1")):
            return False
        return True

    def open(self):
        logging.info("SignallingWebSocket opened from %s", self.request.remote_ip)
        connection_to_recycle = False
        for index, item in enumerate(SignallingWebSocketHandler.clients):
            if item == self:
                SignallingWebSocketHandler.clients[index] = self
                connection_to_recycle = True
                logging.info("SignallingWebSocket recycled connection from %s")
        if not connection_to_recycle:
            SignallingWebSocketHandler.clients.append(self)

        display_manager.wake_up_display()
        super(SignallingWebSocketHandler, self).open()

    def on_message(self, message):
        logging.debug("got message from %s: %s", self.request.remote_ip, message)
        logging.debug("Clients are %d %s", len(SignallingWebSocketHandler.clients), SignallingWebSocketHandler.clients)
        if not message.startswith("ping"):
            for client in SignallingWebSocketHandler.clients:
                if client is not self:
                    logging.debug("Writing msg to %s", message)
                    client.write_message(message)

    def on_close(self):
        logging.info("SignallingWebSocket closed")
        SignallingWebSocketHandler.clients.remove(self)


class LocalSignallingWebSocketHandler(SignallingWebSocketHandler):
    # Overridden for dealing with authentication
    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        if not self.is_local():
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        super(LocalSignallingWebSocketHandler, self).get(*args, **kwargs)


class RemoteSignallingWebSocketHandler(SignallingWebSocketHandler, RootWebSocketHandler):
    pass


class ControlWebSocketHandler(RootWebSocketHandler):
    def initialize(self, _tank):
        self.tank = _tank

    def ping(self, value):
        log.debug("Received a ping responding")
        self.write_message("Pong")

    def set_speed(self, value):
        log.debug("Changing speed to L %s R %s", value[0], value[1])
        self.tank.set_speed(value[0], value[1])
        self.write_message("Setting speed to L %d R %d" % (value[0], value[1]))

    message_types = {
        "ping": ping,
        "speed": set_speed
    }

    def on_message(self, message):
        log.debug("Client received a message : '%s'", message)
        # Parse received json message
        actions = json.loads(message)
        # loop through messages payloads
        for k in actions.keys():
            # Call method with message verb
            self.message_types[k](self, actions[k])

    def on_close(self):
        pass
