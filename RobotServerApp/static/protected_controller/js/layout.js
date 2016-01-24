"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */

// Size of the local video thumbnail
var localImageRatio = 0.15;

// Initialized on startup
var savedGeometry = {
    width: 0,
    height: 0
};

function initDeviceGeometryAndElements() {
    // Get the orientation angle
    var angle = window.orientation.toFixed();
    if (angle == 0 || angle == 180) {
        // Portrait
        savedGeometry.height = window.document.height;
        savedGeometry.width = window.document.width;
    } else {
        // Landscape
        savedGeometry.height = window.document.width;
        savedGeometry.width = window.document.height;
    }
}

function resizeElements() {
    // Get the orientation angle
    var angle = window.orientation.toFixed();
    var i;
    
    console.log(">>> Resize");
    
    if (angle == 0 || angle == 180) {
        // Portrait mode
        // Only work on remote video element
        window.remoteVideo.width = savedGeometry.width;
        window.remoteVideo.height = savedGeometry.height;
    } else {
        // Landscape mode
        // Only work on remote video element
        window.remoteVideo.width = savedGeometry.height;
        window.remoteVideo.height = savedGeometry.width;

    }
    // Resize the local video to the thumbnail size
    window.localVideo.width = window.remoteVideo.width * localImageRatio;
    window.localVideo.height = window.remoteVideo.height * localImageRatio;

    // if iOS devices
    if (window.device.platform === "iOS") {
        // Force redisplay
        console.log(">> Refresh videos");
        cordova.plugins.iosrtc.refreshVideos();
    }
    console.log(">>> Resize R " + window.remoteVideo.width + "x" + window.remoteVideo.height + " L " + window.localVideo.width + "x" + window.localVideo.height);
}

window.addEventListener('orientationchange', function() {
    console.log("Robot app >>> Orientation change");
    var iOS = navigator.userAgent.match(/(iPad|iPhone|iPod)/g);
    var viewportmeta = document.querySelector('meta[name="viewport"]');
    if (iOS && viewportmeta) {
        if (viewportmeta.content.match(/width=device-width/)) {
            viewportmeta.content = viewportmeta.content.replace(/width=[^,]+/, 'width=1');
        }
        viewportmeta.content = viewportmeta.content.replace(/width=[^,]+/, 'width=' + window.innerWidth);
    }
    resizeElements();
}, false); // orientation change
