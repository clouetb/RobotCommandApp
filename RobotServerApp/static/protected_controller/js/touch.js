"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */
var worker = new Worker("control_worker.js");
// Set of fingers
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

document.addEventListener("touchstart", function (event) {
    var i, touch;
    console.log("Touch start");
    event.preventDefault();
    for (i = 0; i < event.changedTouches.length; i++) {
        touch = event.changedTouches[i];
        // Left finger only the first touch
        if ((touch.pageX < (document.width / 2)) && !leftFinger.active) {
            //console.log("touch start on left");
            // Save finger initial state
            leftFinger.id = touch.identifier;
            leftFinger.x = touch.pageX;
            leftFinger.y = touch.pageY;
            leftFinger.active = true;
        // Right finger only the first touch
        } else if ((touch.pageX >= (document.width / 2)) && !rightFinger.active) {
            //console.log("touch start on right");
            // Save finger initial state
            rightFinger.id = touch.identifier;
            rightFinger.x = touch.pageX;
            rightFinger.y = touch.pageY;
            rightFinger.active = true;
        }
    }
}, false); // touch start

// Register touchmove event processing
document.addEventListener("touchmove", function (event) {
    var i, touch;
    event.preventDefault();
    for (i = 0; i < event.changedTouches.length; i++) {
        touch = event.changedTouches[i];
        // Check which finger
        if (leftFinger.id === touch.identifier) {
            // Left finger offset = start position - current position
            leftFinger.offset = leftFinger.y - touch.pageY;
            //console.log("move on left offset " + leftFinger.offset);
        } else if (rightFinger.id === touch.identifier) {
            // Right finger offset = start position - current position
            rightFinger.offset = rightFinger.y - touch.pageY;
            //console.log("move on right offset " + rightFinger.offsetY);
        }
    }
    // Send fingers position to the worker
    worker.postMessage([leftFinger, rightFinger]);
}, false); // touch move

// Register touchend event processing
document.addEventListener("touchend", function (event) {
    var i, touch;
    console.log("Touch end");
    for (i = 0; i < event.changedTouches.length; i++) {
        touch = event.changedTouches[i];
        if (leftFinger.id === touch.identifier) {
            // Reset left finger offset
            leftFinger.offset = 0;
            leftFinger.active = false;
        } else if (rightFinger.id === touch.identifier) {
            // Reset right finger offset
            rightFinger.offset = 0;
            rightFinger.active = false;
        }
    }
    // Send fingers position to the worker
    worker.postMessage([leftFinger, rightFinger]);
}, false); // touch end
