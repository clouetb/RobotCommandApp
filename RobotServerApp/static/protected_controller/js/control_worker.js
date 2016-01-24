"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */

var leftFinger = {
    // Used for later identification
    id: 0,
    x: 0,
    y: 0,
    offset: 0,
    active: false
};
var rightFinger = {
    // Used for later identification
    id: 0,
    x: 0,
    y: 0,
    offset: 0,
    active: false
};
// Number of times a second the position of the fingers will be sent
var fps = 10;
// Socket to the server
var socket = null;

onmessage = function (e) {
    leftFinger = e.data[0];
    rightFinger = e.data[1];
    socket.send(JSON.stringify({
        "speed": [leftFinger.offset,
                  rightFinger.offset]
    }));
};

setInterval(function() {
    var d = new Date();
    //postMessage("Speed L " + leftFinger.offset + " R " + rightFinger.offset + " " + d.yyyymmdd());
    try {
        socket.send(JSON.stringify({
            "speed": [leftFinger.offset,
                      rightFinger.offset]
        }));
    } catch (e) {
        console.log("CW exception was : " + e);
    }
}, Math.round(1000 / fps));

function initCommunication() {
    socket = new WebSocket("wss://" + location.host + "/websocket_control");
    socket.onopen = function () {
        socket.send(JSON.stringify({
            "ping": ""
        }));
    };
    socket.onmessage = function (evt) {
        console.log("Message received: " + String(evt.data));
    };

}

initCommunication();
