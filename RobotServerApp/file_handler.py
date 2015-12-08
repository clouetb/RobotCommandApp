import tornado.web
import tornado.auth
import logging

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class CustomStaticFileHandler(tornado.web.StaticFileHandler):

    # Needed to fetch the authenticated user
    def get_current_user(self):
        return self.get_secure_cookie("user")

    # Just add auth decorator
    @tornado.web.authenticated
    def get(self, path, include_body=True):
        log.debug("Serving for '%s'", self.get_current_user())
        tornado.web.StaticFileHandler.get(self, path, include_body)

