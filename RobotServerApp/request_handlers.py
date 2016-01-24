import tornado.web
import tornado.auth
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class ProtectedHandler(tornado.web.RequestHandler):
    # Needed to fetch the authenticated user
    def get_current_user(self):
        return self.get_secure_cookie("user")

    @tornado.web.asynchronous
    def get(self, *args, **kwargs):
        log.debug("Authenticating request from %s, %s", self.current_user, self.request)
        if not self.current_user:
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        log.debug("Authorized request %s -> %s", self.request.uri, self.request.uri.replace("/controller/", "/protected_controller/"))
        self.set_header('X-Accel-Redirect', self.request.uri.replace("/controller/", "/protected_controller/"))
        self.finish()


class NoAuthHandler(tornado.web.RequestHandler):

    def get(self, path, include_body=True):
        if not ((str(self.request.remote_ip) == "127.0.0.1") or (str(self.request.remote_ip) == "::1")):
            log.warning("Unauthorized user with request %s", self.request)
            self.set_status(403)
            self.finish("Forbidden")
            return
        log.debug("Authorized request %s -> %s", self.request.uri, self.request.uri.replace("/robot/", "/protected_robot/"))
        self.set_header('X-Accel-Redirect', self.request.uri.replace("/robot/", "/protected_robot/"))
        self.finish()
