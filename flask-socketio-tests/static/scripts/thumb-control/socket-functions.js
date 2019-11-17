'use strict';

function emit_xy(x, y) {
    console.log('sending xy message');
    socket_emit_event('xy', {x: x, y: y});
}