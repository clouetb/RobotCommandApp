# RobotCommandApp
Command application for my remote presence robot.
Aims at getting a Raspberry PI to act as a robot with video.

##Requires on the Rpi side
- A model 2 Rpi
- A micro SD card with the vanilla debian
- chromium browser as found here : http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser-l10n_45.0.2454.101-0ubuntu1.1201_all.deb , http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-codecs-ffmpeg_45.0.2454.101-0ubuntu1.1201_armhf.deb , http://ports.ubuntu.com/pool/universe/c/chromium-browser/chromium-browser_45.0.2454.101-0ubuntu1.1201_armhf.deb
- Python with Tornado
- A display for the Rpi
- A webcam (mine is Microsoft HD3000)
- Speakers

##Requires on the mobile side
- Cordova
- The ios RTC plugin https://github.com/eface2face/cordova-plugin-iosrtc

##Todo
###Implement deployment tooling
- See if we can get interesting things from docker or http://robotpkg.openrobots.org/

###For the mobile UI
- Implement the correct lifecycle for re-enabling connection when leaving/re-entering the app --> found a solution but looks brittle
- Find a way to enable HTML elements on the mobile UI (see https://github.com/eface2face/cordova-plugin-iosrtc/issues/38, there is a PR pending...)

###For the Rpi UI
- Enable sound output (input is provided via the webcam)

###For the infrastructure
- Deal with firewalls traversal for enabling communication while not on the same network (https://github.com/miniupnp/miniupnp/)? --> See if this works that well...

###For reducing video latency (which is currently around 1 sec.)
- Enable h.264 on both sides
-- See if the RaspiCam is the solution as it provides a way to spit h.264 directly
-- See if iosrtc is actually offering h.264 as a codec
-- See if a new version of Chromium is required
