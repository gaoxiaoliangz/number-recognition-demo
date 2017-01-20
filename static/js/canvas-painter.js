(function (global) {
  /**
   * http://stackoverflow.com/questions/4817029/whats-the-best-way-to-detect-a-touch-screen-device-using-javascript
   */
  function isTouchDevice() {
    return 'ontouchstart' in window      // works on most browsers 
      || navigator.maxTouchPoints;       // works on IE10/11 and Surface
  }
  function CanvasPainter(canvasDom) {
    // todo: validate if element is canvas
    this._canvas = canvasDom;
    this._context = canvasDom.getContext('2d');

    // initial local state
    this._hasTouch = false;
    this._offsetTop = 0;
    this._offsetLeft = 0;
    this._isDrawing = false;

    this._pointData = {
      x: [],
      y: [],
      r: [],
      ms: []
    };

    this._handleMove = this._handleMove.bind(this);
    this._handleDown = this._handleDown.bind(this);
    this._handleUp = this._handleUp.bind(this);
    this._handleScroll = this._handleScroll.bind(this);
    this._handleResize = this._handleResize.bind(this)

    this._init()
  }

  CanvasPainter.prototype = {
    _init() {
      this._hasTouch = isTouchDevice();
      this._updateOffset();
      this._addListeners();
    },

    _getPointLoc(event) {
      var viewX;
      var viewY;

      if (this._hasTouch) {
        var touches = event.changedTouches;
        viewX = touches[0].clientX
        viewY = touches[0].clientY
      } else {
        viewX = event.clientX
        viewY = event.clientY
      }

      var x = viewX - this._offsetLeft;
      var y = viewY - this._offsetTop;

      return {
        x: x,
        y: y
      }
    },

    _addPainterListeners() {
      var canvas = this._canvas;

      // switch from chrome mobile dev mode to desktop mode
      // hasTouch will still be true causing listeners not be added to canvas
      // this is mainly a dev bug, not gonna fix
      if (!this._hasTouch) {
        canvas.addEventListener('mousemove', this._handleMove, false);
        canvas.addEventListener('mousedown', this._handleDown, false);
        canvas.addEventListener('mouseup', this._handleUp, false);
      } else {
        canvas.addEventListener('touchmove', this._handleMove, false);
        canvas.addEventListener('touchstart', this._handleDown, false);
        canvas.addEventListener('touchend', this._handleUp, false);
      }
    },

    _removePainterListeners() {
      var canvas = this._canvas;
      canvas.removeEventListener('mousemove', this._handleMove, false);
      canvas.removeEventListener('mousedown', this._handleDown, false);
      canvas.removeEventListener('mouseup', this._handleUp, false);
      canvas.removeEventListener('touchmove', this._handleMove, false);
      canvas.removeEventListener('touchstart', this._handleDown, false);
      canvas.removeEventListener('touchend', this._handleUp, false);
    },

    _addListeners() {
      this._addPainterListeners();
      window.addEventListener('scroll', this._handleScroll, false);
      window.addEventListener('resize', this._handleResize, false);
    },

    _removeListeners() {
      this._removePainterListeners();
      window.removeEventListener('scroll', this._handleScroll, false);
      window.removeEventListener('resize', this._handleResize, false);
    },

    _updateOffset() {
      var viewportOffset = this._canvas.getBoundingClientRect();

      this._offsetTop = viewportOffset.top;
      this._offsetLeft = viewportOffset.left;
    },

    _handleScroll(event) {
      this._updateOffset();
    },

    _handleResize() {
      // this._removePainterListeners();
      this._init();
    },

    _handleDown(event) {
      event.preventDefault();
      this._isDrawing = true;
    },

    _handleUp(event) {
      event.preventDefault();
      this._isDrawing = false;
    },

    _handleMove(event) {
      if (!this._hasTouch && !this._isDrawing) {
        return false
      }

      var context = this._context;
      var pointData = this._pointData;
      var ms = new Date();
      var loc = this._getPointLoc(event);
      var x = loc.x;
      var y = loc.y;

      pointData.ms.push(ms);
      pointData.x.push(x);
      pointData.y.push(y);

      var speed = (pointData.x[pointData.x.length - 1] - pointData.x[pointData.x.length - 2]) / (pointData.ms[pointData.ms.length - 1] - pointData.ms[pointData.ms.length - 2]);
      speed = Math.abs(speed);

      var circle_r = 10 - 10 * (speed / (speed + 1));
      pointData.r.push(circle_r);

      // fill path
      function fillPath(a, b) {
        var d = Math.sqrt(Math.pow((b.x - a.x), 2) + Math.pow((b.y - a.y), 2));
        d = Math.floor(d);
        d = d * 3;
        for (var i = 0; i < d; i++) {
          var x = (b.x - a.x) / d * i + a.x;
          var y = (b.y - a.y) / d * i + a.y;
          var r = (b.r - a.r) / d * i + a.r;
          context.beginPath();
          context.arc(x, y, r, 0, Math.PI * 2, true);
          context.closePath();
          context.fill();
        }
      }

      if (pointData.x.length > 2) {
        var p0 = {};
        var p1 = {};
        p0.x = pointData.x[pointData.x.length - 2];
        p1.x = pointData.x[pointData.x.length - 1];
        p0.y = pointData.y[pointData.y.length - 2];
        p1.y = pointData.y[pointData.y.length - 1];
        p0.r = pointData.r[pointData.r.length - 2];
        p1.r = pointData.r[pointData.r.length - 1];
        p0.ms = pointData.ms[pointData.ms.length - 2];
        p1.ms = pointData.ms[pointData.ms.length - 1];
        if (p1.ms - p0.ms < 100) {
          fillPath(p0, p1);
        } else {
          pointData.r[pointData.r.length - 1] = 7;
        }
      }
      event.preventDefault();
    }
  }

  global.CanvasPainter = (canvasDom) => {
    return new CanvasPainter(canvasDom);
  };

} (window));

var CanvasPainter = window.CanvasPainter;

export default CanvasPainter;
