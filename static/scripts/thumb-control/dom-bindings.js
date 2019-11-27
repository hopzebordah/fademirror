'use strict';

const xy_drag_map = document.getElementById('xy-drag-map');
const function_dropdown = document.getElementById('function-dropdown');
const ttl_input = document.getElementById('ttl-input');
const color_picker = document.getElementById('color-input');
const send_button = document.getElementById('send-button');

let nextTickTime = 0;
let dragging = false;
let delay = 75;

window.addEventListener('DOMContentLoaded', (e) => {
    configureColorPicker(color_picker, xy_drag_map);
    configureXYDragMap(xy_drag_map);
});

function configureColorPicker(color_picker, xy_drag_map) {
    let randomColor = "#000000".replace(/0/g,function(){return (~~(Math.random()*16)).toString(16);});
    color_picker.value = randomColor;
    xy_drag_map.style.backgroundColor = randomColor;

    color_picker.addEventListener('change', (e) => {
        let rgb_value = color_picker.value;
        xy_drag_map.style.backgroundColor = rgb_value;
    });
}

function configureXYDragMap(xy_map) {

    xy_map.addEventListener('touchstart', (e) => {
        dragging = true;
    });

    xy_map.addEventListener('touchmove', (e) => mapTouchMoveEventListener(e, xy_map));

    xy_map.addEventListener('touchend', (e) => {
        dragging = false;
    });

}

function mapTouchMoveEventListener(e, xy_map) {
    let date = new Date();
    if (date.getTime() > nextTickTime) {
        if (dragging) {
            calculateAndSendThumbLocation(e.changedTouches[0], xy_map);
            nextTickTime = date.getTime() + delay;
        }
    }
}

function calculateAndSendThumbLocation(event, xy_map) {
    let point = calculateUserTouchPoint(event, xy_map);

    let closestSide = new XYMap().getClosestSide(point);

    let thumbControlData = buildThumbControlObject(closestSide, point.x, point.y);
    emit_thumb_command(thumbControlData);
}

function calculateUserTouchPoint(event, xy_map) {
    let rect = xy_map.getBoundingClientRect();

    let mouseX = event.clientX - rect.left;
    let mouseY = event.clientY - rect.top;

    mouseX = checkBounds(Math.round(mapRange(mouseX, 0, (rect.right - rect.left), 0, 100)));
    mouseY = 100 - checkBounds(Math.round(mapRange(mouseY, 0, (rect.bottom - rect.top), 0, 100)));

    if (DEBUG)
        console.log(mouseX + ':' + mouseY);

    if (isNaN(mouseX) || isNaN(mouseY))
        return;

    return new Point(mouseX, mouseY);
}

function buildThumbControlObject(side, x, y) {
    const position = getPositionAccordingToSide(side, x, y);
    const func = function_dropdown.value;
    const ttl = Number(ttl_input.value);
    const rgb = color_picker.value;
    return new ThumbControlData(side, position, func, ttl, rgb);
}

function getPositionAccordingToSide(side, x, y) {
    let position;
    if (side === 'top' || side === 'bottom')
        position = x;
    else 
        position = y;
    return position;
}

function checkBounds(val) {
    if (val > 100)
        return 100;
    if (val < 0)
        return 0;
    return val;
}