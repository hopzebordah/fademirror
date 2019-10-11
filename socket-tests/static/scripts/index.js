'use strict';

// class for transferring data to websocket
class wsMessage {
    constructor(type, data) {
        this.type = type; 
        this.data = data;
    }
}

// connect to separate websocket server
let webSocket = new WebSocket('ws://127.0.0.1:5001/');

// TODO: hold off on configuring ui elements from interacting with websocket until websocket is loaded.
// we just need to wait for a connnection established method as well as the domcontentloaded event 

// log a message when we receive it from the websocket server
webSocket.onmessage = (e) => {
    console.log('MESSAGE FROM WS SERVER: ' + e.data);
};

// configure ui elements
window.addEventListener('DOMContentLoaded', (e) => {
    const singleClickButton = document.getElementById('single-click-btn');
    configureSingleClickButton(singleClickButton);

    const dropdown = document.getElementById('dropdown');
    const dropdownSubmit = document.getElementById('dropdown-submit');
    configureDropdown(dropdown, dropdownSubmit);

    const multipleClickButton = document.getElementById('multiple-click-btn');
    configureMultipleClickButton(multipleClickButton);

    const xyMap = document.getElementById('xyMap');
    configureXYMap(xyMap);
});

function configureSingleClickButton(singleClickButton) {
    singleClickButton.onclick = (e) => {
        let clickMessage = new wsMessage('clickMessage', 'single click button pressed!');
        webSocket.send(JSON.stringify(clickMessage));
    };
}

function configureDropdown(dropdown, dropdownSubmit) {
    dropdownSubmit.onclick = (e) => {
        let selected = dropdown.value;
        let dropdownMessage = new wsMessage('dropdownMessage', selected);
        webSocket.send(JSON.stringify(dropdownMessage));
    };
}

// TODO: change this from onclick to drag somehow
function configureMultipleClickButton(multipleClickButton) {
    multipleClickButton.onclick = (e) => {
        for (let i=0; i<10; i++) {
            let multipleClickMessage = new wsMessage('multipleClickMessage', i);
            webSocket.send(JSON.stringify(multipleClickMessage));
        }
    };
}

function configureXYMap(xyMap) {
    xyMap.onclick = (e) => {
        let rect = xyMap.getBoundingClientRect();
        let mouseX = e.clientX - rect.left;
        let mouseY = e.clientY - rect.top;
        mouseX = Math.round(mapRange(mouseX, 0, (rect.right - rect.left), 0, 100));
        mouseY = Math.round(mapRange(mouseY, 0, (rect.bottom - rect.top), 0, 100));
        console.log(mouseX + ':' + mouseY);

        let xyMapMessage = new wsMessage('xyMap', {mouseX, mouseY});
        webSocket.send(JSON.stringify(xyMapMessage));
    };
}

function mapRange(value, low1, high1, low2, high2) {
    return low2 + (high2 - low2) * (value - low1) / (high1 - low1);
}