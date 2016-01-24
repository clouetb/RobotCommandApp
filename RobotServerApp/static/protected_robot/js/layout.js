"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */
console.log("Videos : " + window.remoteVideo + " " + window.localVideo);

// Size of the local video thumbnail
var localImageRatio = 0.15;

// Initialized on startup
var savedGeometry = {
    width: 0,
    height: 0
};

function initDeviceGeometryAndElements() {
    savedGeometry.height = $(window).height();
    savedGeometry.width = $(window).width();
    console.log("Geom " + savedGeometry);
}

function resizeElements() {
    // Only work on remote video element
    window.remoteVideo.width = savedGeometry.width;
    window.remoteVideo.height = savedGeometry.height;
    // Resize the local video to the thumbnail size
    window.localVideo.width = window.remoteVideo.width * localImageRatio;
    window.localVideo.height = window.remoteVideo.height * localImageRatio;
    console.log(">>> Resize R " + window.remoteVideo.width + "x" + remoteVideo.height + " L " + localVideo.width + "x" + localVideo.height);
}
