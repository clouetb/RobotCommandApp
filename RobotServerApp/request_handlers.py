import tornado.web
import tornado.auth
import logging


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class RootHandler(tornado.web.RequestHandler):
    # Needed to fetch the authenticated user
    def get_current_user(self):
        return self.get_secure_cookie("user")


class CustomStaticFileHandler(tornado.web.StaticFileHandler, RootHandler):
    # Just add auth decorator
    @tornado.web.authenticated
    def get(self, path, include_body=True):
        tornado.web.StaticFileHandler.get(self, path, include_body)
