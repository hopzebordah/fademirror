'use strict';

function emit_thumb_command(thumbControlData) {
    console.log('sending thumb control command');
    socket_emit_event('thumb_control', thumbControlData);
}

function emit_xy(x, y) {
    console.log('sending xy message');
    socket_emit_event('xy', {x: x, y: y});
}