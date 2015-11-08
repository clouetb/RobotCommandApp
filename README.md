# RobotCommandApp
Command application for my remote presence robot.
Aims at getting a Raspberry PI to act as a robot with video.

##Requires on the Rpi side
- A model 2 Rpi
- A micro SD card with the vanilla debian
- chromium browser as found here : http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser-l10n_45.0.2454.101-0ubuntu1.1201_all.deb , http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg_45.0.2454.101-0ubuntu1.1201_armhf.deb , http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser_45.0.2454.101-0ubuntu1.1201_armhf.deb
- Nodejs as found here : http://node-arm.herokuapp.com/node_latest_armhf.deb
- A display for the Rpi
- Speakers

##Requires on the mobile side
- Cordova
- The ios RTC plugin https://github.com/eface2face/cordova-plugin-iosrtc

##Additional notes
###For the mobile UI
- See how to make remote view expand on the whole screen
- See how to make local view overlay on the remote view
- See how to implement sliders for driving the tank threads
- See how to deal with orientation changes

###For the Rpi UI
- Implement startup UI (See http://blogs.wcode.org/2013/09/howto-boot-your-raspberry-pi-into-a-fullscreen-browser-kiosk/)
