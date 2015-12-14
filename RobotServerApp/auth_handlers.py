import tornado.web
import tornado.auth
import logging
import json

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

redirect_url = "https://robot-pi.bclouet.eu:8888/auth"


class LoginHandler(tornado.web.RequestHandler,
                   tornado.auth.GoogleOAuth2Mixin):

    # Called twice during the auth process
    @tornado.gen.coroutine
    def get(self):
        # Authenticated user comes with a code argument
        if not self.get_argument("code", False):
            # 1st call : user is NOT authenticated and should be sent to the auth page at Google
            log.debug("Unauthenticated user, sending to auth page, then sending to '%s'", self.get_argument("next", "/ (default param)"))
            # Save the URL the user was asking for
            self.set_cookie("next", self.get_argument("next", "/index.html"))
            # Send user to the auth page
            yield self.authorize_redirect(
                # Callback URL (should be this same URL)
                redirect_uri=redirect_url,
                # Id of the OAuth client @ Google
                client_id=self.settings["google_oauth"]["key"],
                # What we would like to fetch (and ask the user's consent for)
                scope=["profile", "email"],
                # Response should be provided as an OAuth code
                response_type="code",
                extra_params={"approval_prompt": "auto"})
        else:
            # 2nd call : user comes back from auth page at Google, with an OAuth code
            # Get user reference at Google OAuth website
            user = yield self.get_authenticated_user(
                                        redirect_uri=redirect_url,
                                        code=self.get_argument("code"))
            # Extract access token from the reference
            access_token = str(user["access_token"])
            log.debug("Access token %s", self.get_argument("code", False))
            http_client = self.get_auth_http_client()
            # Fetch user's profile from google, using the token he provided as a mark of his consent
            response = yield \
                http_client.fetch("https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + access_token)
            # Problem during fetch
            if not response:
                self.clear_all_cookies()
                raise tornado.web.HTTPError(500, "Google authentication failed")
            # Response is provided as Json
            user = json.loads(response.body)
            log.debug("Current user is %s", user)
            # Save the username as a secure cookie
            self.set_secure_cookie("user", user["email"])
            # Send the user to the URL he intended to reach before having to authenticate
            next_url = self.get_cookie("next")
            log.debug("Next url is %s", next_url)
            self.redirect(next_url)


class LogoutHandler(tornado.web.RequestHandler):

    @tornado.gen.coroutine
    def get(self):
        self.clear_all_cookies()
        self.write("You are now logged out")

