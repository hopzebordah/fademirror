'use strict';

function emit_thumb_command(thumbControlData) {
    if (DEBUG)
        console.log('sending thumb control command');
    socket_emit_event('thumb_control', thumbControlData);
}

function emit_clear() {
    if (DEBUG)
        console.log('sending clear command');
    socket_emit_event('clear');
}

function emit_xy(x, y) {
    if (DEBUG)
        console.log('sending xy message');
    socket_emit_event('xy', {x: x, y: y});
}