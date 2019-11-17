'use strict';

window.addEventListener('DOMContentLoaded', (e) => {
    const xyMap = document.getElementById('xyMap');
    configureXYMap(xyMap, 'click');
    configureXYMap(xyMap, 'touchstart');
});

function configureXYMap(xyMap, event_type) {
    xyMap.addEventListener(event_type, (e) => {
        let rect = xyMap.getBoundingClientRect();
        let mouseX = e.clientX - rect.left;
        let mouseY = e.clientY - rect.top;

        mouseX = Math.round(mapRange(mouseX, 0, (rect.right - rect.left), 0, 100));
        mouseY = Math.round(mapRange(mouseY, 0, (rect.bottom - rect.top), 0, 100));

        if (isNaN(mouseX) || isNaN(mouseY))
            return;

        console.log(mouseX + ':' + mouseY);

        emit_xy(mouseX, mouseY);
    });
}