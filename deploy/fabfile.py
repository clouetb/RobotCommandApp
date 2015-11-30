from fabric.operations import *
from fabric.api import *
from fabric.context_managers import *
LOCAL_DIR = "/Users/benoitclouet/Documents/RobotCommandApp/RobotServerApp"
REMOTE_DIR = "/home/pi/RobotCommandApp"
APP_ROOT = os.path.join(REMOTE_DIR, "RobotServerApp")

env.hosts = ["pi@robot-pi.local"]


def deploy():
    put(local_path=LOCAL_DIR, remote_path=REMOTE_DIR)


def populate_var():
    for executable in ["robot-pi", "chromium-browser"]:
        for directory in ["log", "run"]:
            sudo("mkdir -p /var/%s/%s" % (directory, executable))
            sudo("chown -R pi:pi /var/%s/%s" % (directory, executable))


def start_browser():
    with cd(APP_ROOT):
        run("./chromium start")


def stop_browser():
    with cd(APP_ROOT):
        run("./chromium stop")


def refresh_browser():
    with cd(APP_ROOT):
        run("./chromium refresh")


def start_server():
    with cd(APP_ROOT):
        run("./robot-pi start")


def stop_server():
    with cd(APP_ROOT):
        run("./robot-pi stop")


def restart_server():
    stop_server()
    start_server()


def restart_browser():
    stop_browser()
    start_browser()


def log_server():
    run("tail -f /var/log/robot-pi/robot-pi.log")


def log_browser():
    run("tail -f /var/log/chromium-browser/chromium-browser.log")
