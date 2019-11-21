'use strict';

class Point {

    constructor(x, y) {
        this.x = x;
        this.y = y;
    }

    isAbove(other) {
        if (this.y >= other.y)
            return true;
        return false;
    }

}