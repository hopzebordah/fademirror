'use strict';

var socket = io();

socket.on('connect', function() {
    emit_connected();
});

socket.on('ack', (data) => {
    if (DEBUG) {
        console.log('[+] received ack!')
        console.log('data: ' + data)
    }
});

function emit_connected() {
    socket_emit_event('connected', {});
}

function socket_emit_event(event_name, event_data) {
    if (DEBUG) 
        console.log('[+] emitting ' + event_name);
    socket.emit(event_name, event_data);
}