"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */
var url = "wss://" + location.host + "/websocket_robot_signaling";
var ws = new WebSocket(url);
var pc;
var localStream;
var remoteStream;
var isStarted;
var turnReady;

var pc_config = {'iceServers': [{'url': 'stun:stun.l.google.com:19302'}]};

var pc_constraints = {
	'optional': [
		{'DtlsSrtpKeyAgreement': true},
		{'RtpDataChannels': true}
	]
};

// Set up audio and video regardless of what devices are present.
var sdpConstraints = {'mandatory': {'OfferToReceiveAudio': true,
                                    'OfferToReceiveVideo': true}
                     };

// Keep signalling websocket alive
setInterval(function() {
    if (ws.readyState > 1) {
        console.log("Socket closed, reloading...");
        location.reload(true);
    } else {
        ws.send("ping");
    }
}, 2000);

function fail(e) {
    console.error(e);
}

function receiveOffer(offer) {
    console.log('received offer...');
    pc.setRemoteDescription(new RTCSessionDescription(offer), function () {
        console.log('creating answer...');
        pc.createAnswer(function (answer) {
            console.log('created answer...');
            pc.setLocalDescription(answer, function () {
                console.log('sent answer');
                ws.send(JSON.stringify(answer));
            }, fail);
        }, fail, sdpConstraints);
    }, fail);
}

function connect(stream) {
    pc = new RTCPeerConnection(pc_config, pc_constraints);
	console.log("Created local peer connection");
	
    if (stream) {
        pc.addStream(stream);
        var video = document.getElementById('local');
        video.src = URL.createObjectURL(stream);
        resizeElements();
        //attachMediaStream($('#local'), stream);
    }
    
    pc.onaddstream = function (event) {
        var video = document.getElementById('remote');
        video.src = URL.createObjectURL(event.stream);
        resizeElements();
        //attachMediaStream($('#remote'), event.stream);
    };

    pc.onicecandidate = function (event) {
        if (event.candidate) {
            ws.send(JSON.stringify(event.candidate));
        }
    };
    
    ws.onmessage = function (event) {
        if (event.data === "disconnect"){
            console.log("Received a diconnect instruction, reloading");
            location.reload(true);
            return;
        }
        var signal = JSON.parse(event.data);
        console.log(">>> Signal : " + event.data);
        if (signal.sdp) {
            receiveOffer(signal);
        } else if (signal.candidate) {
            pc.addIceCandidate(new RTCIceCandidate(signal));
        }
    };
}

function init() {
    var constraints = {
        audio: true,
        video: true
    };
    getUserMedia(constraints, connect, fail);
}