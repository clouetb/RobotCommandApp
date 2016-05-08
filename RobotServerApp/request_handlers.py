import tornado.web
import tornado.auth
import logging

from turn_server_manager import TurnServerManager

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class RootHandler(tornado.web.RequestHandler):

    def is_local(self):
        if not ((str(self.request.headers.get('X-Forwarded-For')) == "127.0.0.1") or
                    (str(self.request.headers.get('X-Forwarded-For')) == "::1")):
            return False
        return True

    # Needed to fetch the authenticated user
    def get_current_user(self):
        return self.get_secure_cookie("user")

class ProtectedHandler(RootHandler):

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        log.debug("Authenticating request from %s, %s", self.current_user, self.request)
        if not self.current_user:
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        log.debug("Authorized request %s -> %s",
                  self.request.uri,
                  self.request.uri.replace("/controller/", "/protected_controller/"))
        self.set_header('X-Accel-Redirect',
                        self.request.uri.replace("/controller/", "/protected_controller/"))
        self.finish()


class NoAuthHandler(RootHandler):

    @tornado.web.asynchronous
    def get(self, path, include_body=True):
        log.debug("Non authenticated request : %s", self.request)
        if not self.is_local():
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        log.debug("Authorized request %s -> %s",
                  self.request.uri,
                  self.request.uri.replace("/robot/", "/protected_robot/"))
        self.set_header('X-Accel-Redirect',
                        self.request.uri.replace("/robot/", "/protected_robot/"))
        self.finish()


class ConfigurationRequestHandler(RootHandler):

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        if not (self.is_local() or self.current_user):
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        signalling_configuration = TurnServerManager.instance.get_signalling_configuration()
        log.debug("Signalling configuration : %s", signalling_configuration)
        self.set_header('Content-Type', 'application/json')
        self.write(signalling_configuration)
        self.finish()