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
- SimpleWebRTC https://github.com/andyet/SimpleWebRTC

##Todo
###Implement deployment tooling
- On the mobile UI
- Basic deployment automation on the RPi

###For the mobile UI
- See how to implement sliders for driving the tank threads
    Deal with the freeze of the events when fingers are touching the screen
- Implement the correct lifecycle for re-enabling connection when leaving/re-entering the app

###For the Rpi UI
- Implement startup UI (See http://blogs.wcode.org/2013/09/howto-boot-your-raspberry-pi-into-a-fullscreen-browser-kiosk/)
- Enable sound output (input is provided via the webcam)
- Enable some kind of authentication for the tornado server (must be supported on the client side)
    Maybe a certificate based authentication ?

###For the infrastructure
- Become independent of the public signalmaster for security reasons
- Deal with firewalls traversal for enabling communication while not on the same network