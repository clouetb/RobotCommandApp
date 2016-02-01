import logging
import shlex
import subprocess
import websocket_handler

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def wake_up_display():
    if websocket_handler.SignallingWebSocketHandler.clients.count() == 2:
        cmdline = "xset -display :0 dpms force on"
        args = shlex.split(cmdline)
        log.debug("Waking up display with cmdline : %s", args)
        subprocess.call(args)
