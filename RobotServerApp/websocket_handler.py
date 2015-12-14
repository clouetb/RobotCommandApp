import json
import logging
import tornado.websocket

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class WebSocketHandler(tornado.websocket.WebSocketHandler):

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
            self.set_status(401)
            self.finish("Unauthorized")
            return
        log.debug("User is %s", self.get_current_user())
        # Continue websocket handshake
        super(WebSocketHandler, self).get(*args, **kwargs)

    # Needed for making secure cross-domain websockets to work
    def check_origin(self, origin):
        return True

    def open(self, *args):
        log.debug("Connection incomming")
        self.stream.set_nodelay(True)

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
