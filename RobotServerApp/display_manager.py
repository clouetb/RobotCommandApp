import logging
import shlex
import subprocess


log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def wake_up_display():
    cmdline = "xset -display :0 dpms force on"
    args = shlex.split(cmdline)
    log.debug("Waking up display with cmdline : %s", args)
    process = subprocess.Popen(args, stdout=subprocess.PIPE)
