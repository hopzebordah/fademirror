'use strict';

class ThumbControlData {
    constructor(x, y, mode, ttl, rgb) {
        this.x = x; // should be int
        this.y = y; // should be int
        this.mode = mode; // should be string (or enum)
        this.ttl = ttl; // should be int (time to live)
        this.rgb = rgb; // should be int (or whatever html widget returns)
    }
}