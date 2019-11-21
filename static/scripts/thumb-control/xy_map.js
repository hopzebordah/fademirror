'use strict';

class XYMap {

    f(x) {
        return new Point(x, x);
    }

    g(x) {
        return new Point(x, 100 - x);
    }

    getClosestSide(point) {
        let point_f = this.f(point.x);
        let point_g = this.g(point.x);
        
        let is_above_f = point.isAbove(point_f);
        let is_above_g = point.isAbove(point_g);

        if (is_above_f && is_above_g)
            return 'top';
        if (is_above_f && !is_above_g)
            return 'left';
        if (!is_above_f && is_above_g)
            return 'right';
        return 'bottom';
    }

}