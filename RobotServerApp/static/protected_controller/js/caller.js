"use strict";
/*jslint vars: true, plusplus: false, devel: true, nomen: true, indent: 4, maxerr: 50 */
/*global define */
var ws = new FakeWebSocket("wss://" + location.host + "/websocket_controller_signaling");
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

function fail(e) {
    console.error(e);
}

function createOffer() {
    console.log('creating offer...');
    pc.createOffer(function (offer) {
        console.log('created offer...');
        pc.setLocalDescription(offer, function () {
            console.log('sending to remote...');
            ws.send(JSON.stringify(offer));
        }, fail);
    }, fail, sdpConstraints);
    resizeElements();
}

function receiveAnswer(answer) {
    console.log('received answer');
    pc.setRemoteDescription(new RTCSessionDescription(answer));
    resizeElements();
}

function connect(stream) {
    pc = new RTCPeerConnection(pc_config, pc_constraints);
	console.log("Created local peer connection");
	
    if (stream) {
        pc.addStream(stream);
        var video = document.getElementById('local');
        video.src = URL.createObjectURL(stream);
        console.log("Local is " + video.src);
        resizeElements();
    }
    
    pc.onaddstream = function (event) {
        var video = document.getElementById('remote');
        video.src = URL.createObjectURL(event.stream);
        console.log("Remote is " + video.src);
        resizeElements();
    };

    pc.onicecandidate = function (event) {
        if (event.candidate) {
            ws.send(JSON.stringify(event.candidate));
        }
        resizeElements();
    };

    ws.onmessage = function (event) {
        var signal = JSON.parse(event.data);
        if (signal.sdp) {
            receiveAnswer(signal);
        } else if (signal.candidate) {
            pc.addIceCandidate(new RTCIceCandidate(signal));
        }
    };   
    createOffer();
}

// To be called once all is ready
function init() {
    var constraints = {
        audio: true,
        video: true
    };
    cordova.plugins.iosrtc.getUserMedia(constraints, connect, fail);
    resizeElements();
}