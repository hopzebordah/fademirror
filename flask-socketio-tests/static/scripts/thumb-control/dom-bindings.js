'use strict';

const xy_drag_map = document.getElementById('xy-drag-map');
const function_dropdown = document.getElementById('function-dropdown');
const ttl_input = document.getElementById('ttl-input');
const color_picker = document.getElementById('color-input');
const send_button = document.getElementById('send-button');

let nextTickTime = 0;

let dragging = false;

window.addEventListener('DOMContentLoaded', (e) => {
    configureXYDragMap(xy_drag_map);
    configureColorPicker(color_picker, xy_drag_map);
});

function configureXYDragMap(xy_map) {

    xy_map.addEventListener('touchstart', (e) => {
        dragging = true;
    });

    xy_map.addEventListener('touchmove', (e) => {
        let date = new Date();
        if (date.getTime() > nextTickTime) {
            if (dragging) {
                calculateAndSendThumbLocation(e.changedTouches[0], xy_map);
                nextTickTime = date.getTime() + 125;
            }
        }
    });

    xy_map.addEventListener('touchend', (e) => {
        dragging = false;
    });

}

function calculateAndSendThumbLocation(event, xy_map) {
    let rect = xy_map.getBoundingClientRect();

    let mouseX = event.clientX - rect.left;
    let mouseY = event.clientY - rect.top;

    mouseX = Math.round(mapRange(mouseX, 0, (rect.right - rect.left), 0, 100));
    mouseY = Math.round(mapRange(mouseY, 0, (rect.bottom - rect.top), 0, 100));

    if (isNaN(mouseX) || isNaN(mouseY))
        return;

    if (mouseX > 100)
        mouseX = 100;
    if (mouseX < 0) 
        mouseX = 0;
    if (mouseY > 100) 
        mouseY = 100;
    if (mouseY < 0) 
        mouseY = 0;

    if (DEBUG)
        console.log(mouseX + ':' + mouseY);

    let thumbControlData = buildThumbControlObject(mouseX, mouseY);
    emit_thumb_command(thumbControlData);
}

function configureColorPicker(color_picker, xy_drag_map) {

    let randomColor = "#000000".replace(/0/g,function(){return (~~(Math.random()*16)).toString(16);});
    color_picker.value = randomColor;
    xy_drag_map.style.backgroundColor = randomColor;

    color_picker.addEventListener('change', (e) => {
        let rgb_value = color_picker.value;
        xy_drag_map.style.backgroundColor = rgb_value;
    });
}

function buildThumbControlObject(x, y) {
    const func = function_dropdown.value;
    const ttl = Number(ttl_input.value);
    const rgb = color_picker.value;
    return new ThumbControlData(x, y, func, ttl, rgb);
}