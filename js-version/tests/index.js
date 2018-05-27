var inherits = require('inherits');
var Readable = require('readable-stream').Readable;

var nextTick = typeof setImmediate !== 'undefined'
    ? setImmediate : process.nextTick
;

function AudioStream(opts, fn)
{
	Readable.call(this);
    
    this.readable = true;
    this.rate = opts.rate || 44000;
    this._fn = fn;
    
    this.t = 0;
    this.i = 0;
    
    this._ticks = 0;
}


inherits(AudioStream, Readable)


AudioStream.prototype._read = function read (bytes) {
    if (!bytes) bytes = 4096;
    var self = this;
    
    var buf = new Buffer(Math.floor(bytes));
    function clamp (x) {
        return Math.max(Math.min(x, Math.pow(2,15)-1), -Math.pow(2,15));
    }
    
    for (var i = 0; i < buf.length; i += 2) {
        var t = self.t + Math.floor(i / 2) / self.rate;
        var counter = self.i + Math.floor(i / 2);
        
        var n = this._fn.call(self, t, counter);
        if (isNaN(n)) n = 0;
        buf.writeInt16LE(clamp(signed(n)), i);
    }
    
    self.i += buf.length / 2;
    self.t += buf.length / 2 / self.rate;
    
    self._ticks ++;
    if (!self._ended && self._ticks % 50) this.push(buf);
    else if (!self._ended) nextTick(function () { self.push(buf) });
};
function signed (n) {
    if (isNaN(n)) return 0;
    var b = Math.pow(2, 15);
    return n > 0
        ? Math.min(b - 1, Math.floor((b * n) - 1))
        : Math.max(-b, Math.ceil((b * n) - 1))
    ;
}
function fn(t,i) { return Math.sin(Math.PI*2.0*440.0*t);}
var audio_stream = new AudioStream( {}, fn );

audio_stream.pipe(process.stdout);