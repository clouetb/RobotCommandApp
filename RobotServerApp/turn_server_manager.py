import base64
import hashlib
import hmac
import json
import logging
import shlex
import subprocess
import time

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class TurnServerManager:

    instance = None

    def __init__(self, cert=None,
                 key=None,
                 internal_ip=None,
                 external_ip=None,
                 realm=None,
                 secret=None,
                 other_options=None):
        self.cert = cert
        self.key = key
        self.internal_ip = internal_ip
        self.external_ip = external_ip
        self.realm = realm
        self.secret = secret
        self.other_options = other_options
        self.raw_cmdline = None
        self.process = None
        TurnServerManager.instance = self

    def get_cmdline(self):
        cmdline = "/usr/bin/turnserver"
        if self.other_options:
            cmdline += " " + self.other_options + " "
        if self.cert:
            cmdline += (" --cert %s " % self.cert)
        if self.key:
            cmdline += (" --pkey %s " % self.key)
        if self.external_ip and self.internal_ip:
            cmdline += (" -X %s/%s " % (self.external_ip, self.internal_ip))
        if self.realm:
            cmdline += (" --realm %s " % self.realm)
        if self.secret:
            cmdline += (" --static-auth-secret %s " % self.secret)
        return cmdline

    def start_turn_server(self):
        args = shlex.split(self.raw_cmdline or self.get_cmdline())
        log.debug("Turn server process arguments : %s", args)
        self.process = subprocess.Popen(args, stdout=subprocess.PIPE)
        log.info("Turn server process started")

    def stop_turn_server(self):
        self.process.terminate()

    def get_signalling_configuration(self):
        digester = hmac.new(self.secret, digestmod=hashlib.sha1)
        username = str(int(round(time.time())) + 86400)
        digester.update(username)
        password = base64.b64encode(digester.digest()).decode("ascii")
        return json.dumps(dict(iceServers=[dict(url="stun:stun.l.google.com:19302"),
                           dict(url="turn:" + self.realm, username=username, credential=password)]))
