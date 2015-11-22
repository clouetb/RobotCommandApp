#!/bin/bash

SSH_TARGET=pi@robot-pi.local
DEPLOY_LOCAL_DIR=/Users/benoitclouet/Documents/RobotCommandApp/RobotServerApp
DEPLOY_REMOTE_DIR=/home/pi/RobotCommandApp

function deploy {
    scp -r ${DEPLOY_LOCAL_DIR} ${SSH_TARGET}:${DEPLOY_REMOTE_DIR}
}

function execute {
    ssh ${SSH_TARGET} << __ENDSSH__
export DISPLAY=:0
xhost +

# Only execute new instance of chromium when not already running
CHROMIUM=\$(ps ax|grep kiosk|grep -v grep)
if [ ! "\${CHROMIUM}" ] 
then 
    chromium-browser --kiosk https://robot-pi.local:8888/index.html&
else
    # Otherwise refresh browser page
    WID=\$(xdotool search --onlyvisible --class chromium|head -1)
    xdotool windowactivate \${WID}
    xdotool key ctrl+F5 
fi

# Kill python if already running
PYTHON=\$(ps ax | grep "python server.py" | grep -v grep | awk '{print $1}')
echo \${PYTHON}
if [ "\${PYTHON}" ] 
then 
    kill \${PYTHON}
fi

# Go into directory
cd ${DEPLOY_REMOTE_DIR}/RobotServerApp

# Run
python server.py
__ENDSSH__

}

function refresh {
    ssh ${SSH_TARGET} << __ENDSSH__
export DISPLAY=:0
xhost +
WID=\$(xdotool search --onlyvisible --class chromium|head -1)
xdotool windowactivate \${WID}
xdotool key ctrl+F5
__ENDSSH__
}

ARGS=$@
if [ ${#ARGS[@]} -eq 0 ]
then
    ARGS="usage"
fi

for var in $ARGS
do
    case $var in
        deploy)
            deploy
            ;;
        execute)
            execute
            ;;
        refresh)
            refresh
            ;;
        *)
            echo "Usage : $0 {deploy|execute|refresh}+"
            ;;
    esac
done
