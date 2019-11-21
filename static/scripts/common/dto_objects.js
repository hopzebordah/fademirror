'use strict';

class ThumbControlData {
    constructor(side, position, mode, ttl, rgb) {
        this.side = side; // the side that the user touched
        this.position = position; // int indicating where on the side
        this.mode = mode; // should be string (or enum)
        this.ttl = ttl; // should be int (time to live)
        this.rgb = rgb; // should be int (or whatever html widget returns)
    }
}