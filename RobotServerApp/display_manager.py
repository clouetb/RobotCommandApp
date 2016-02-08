import logging
import shlex
import subprocess
import websocket_handler

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def wake_up_display():
    # Wake up display only if there is a client connected (the robot is the first client)
    if len(websocket_handler.SignallingWebSocketHandler.clients) > 1:
        cmdline = "xset -display :0 dpms force on"
        args = shlex.split(cmdline)
        log.debug("Waking up display with cmdline : %s", args)
        subprocess.call(args)
