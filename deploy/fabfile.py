from fabric.operations import *
from fabric.api import *
from fabric.context_managers import *
LOCAL_DIR = "/Users/benoitclouet/Documents/RobotCommandApp/RobotServerApp"
REMOTE_DIR = "/home/pi/RobotCommandApp"
APP_ROOT = os.path.join(REMOTE_DIR, "RobotServerApp")

env.hosts = ["pi@robot-pi.bclouet.eu"]


def deploy():
    put(local_path=LOCAL_DIR, remote_path=REMOTE_DIR)
    run("ln -sf /home/pi/RobotCommandApp/ssl_stuff /home/pi/RobotCommandApp/RobotServerApp/ssl_stuff")
    with cd(APP_ROOT):
        for executable in ["robot-pi", "chromium", "server.py"]:
            run("chmod a+x %s" % executable)


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


def start_tornado():
    with cd(APP_ROOT):
        run("./robot-pi start")


def stop_tornado():
    with cd(APP_ROOT):
        run("./robot-pi stop")


def restart_tornado():
    stop_tornado()
    start_tornado()


def start_nginx():
    run("sudo service nginx start")


def stop_nginx():
    run("sudo service nginx stop")


def restart_tornado():
    run("sudo service nginx restart")


def restart_browser():
    stop_browser()
    start_browser()


def log_tornado():
    run("tail -n 100 -f /var/log/robot-pi/robot-pi.log")


def log_browser():
    run("tail -f /var/log/chromium-browser/chromium-browser.log")
