from fabric.operations import *
from fabric.api import *
from fabric.context_managers import *
LOCAL_DIR = "/Users/benoitclouet/Documents/RobotCommandApp/RobotServerApp"
REMOTE_DIR = "/home/pi/RobotCommandApp"
APP_ROOT = os.path.join(REMOTE_DIR, "RobotServerApp")

env.hosts = ["pi@robot-pi.local"]

def deploy():
    put(local_path=LOCAL_DIR, remote_path=REMOTE_DIR)


def start():
    with cd(APP_ROOT):
        run("./robot-pi start")


def stop():
    with cd(APP_ROOT):
        run("./robot-pi stop")


def restart():
    stop()
    start()


def log():
    run("tail -f /var/log/robot-pi/robot-pi.log")


