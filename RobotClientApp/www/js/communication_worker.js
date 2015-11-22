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

var fps = 1;

var socket = null;

onmessage = function(e) {
    leftFinger = e.data[0];
    rightFinger = e.data[1];
    socket.send(JSON.stringify({
        "speed":[leftFinger.offset, 
                rightFinger.offset]
    }));
}

Date.prototype.yyyymmdd = function() {
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth() + 1).toString(); // getMonth() is zero-based
    var dd = this.getDate().toString();
    var hh = this.getHours().toString();
    var min = this.getMinutes().toString();
    var ss = this.getSeconds().toString();
    return yyyy + (mm[1] ? mm : "0" + mm[0]) + (dd[1] ? dd : "0" + dd[0]) + (hh[1] ? hh : "0" + hh) + (min[1] ? min : "0" + min) + (ss[1] ? ss : "0" + ss); // padding
};

setInterval(function() {
    //d = new Date();
    //postMessage("Speed L " + leftFinger.offset + " R " + rightFinger.offset + " " + d.yyyymmdd());
    socket.send(JSON.stringify({
        "speed":[leftFinger.offset, 
                rightFinger.offset]
    }));
}, Math.round(1000/fps));

function initCommunication() {
    socket = new WebSocket("wss://robot-pi.local:8888/socket");
    socket.onopen = function() {
        socket.send(JSON.stringify({
            "ping": ""
        }));
    };
/*
    socket.onmessage = function(evt) {
        postMessage("Message received: " + evt.data);
    };
*/
}

initCommunication();
