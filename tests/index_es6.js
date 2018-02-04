'use strict';
var inherits = require('inherits');
var Readable = require('readable-stream').Readable;

class AudioStream extends Readable
{
    constructor(fn) 
    {
        super();
        this.readable = true;
        this.rate = 44000;
        this._fn = fn;
        
        this.t = 0;
        this.i = 0;
        
        this._ticks = 0;        
        this.buffer = null;
    }

    _read(bytes) 
    {

        function clamp (x) 
        {
            return Math.max(Math.min(x, Math.pow(2,15)-1), - Math.pow(2,15));
        }
        function signed (n) 
        {
            if (isNaN(n)) return 0;
            var b = Math.pow(2, 15);
            return n > 0
                ? Math.min(b - 1, Math.floor((b * n) - 1))
                : Math.max(-b, Math.ceil((b * n) - 1));
        }        
        console.warn(bytes);
        if (!bytes) bytes = 4096;
        if (this.buffer === null) 
        {
            this.buffer = new Buffer(Math.floor(bytes)); 
        }
        var self = this;
        
        //var buffer = new Buffer(Math.floor(bytes));
        
        for (var i = 0; i < self.buffer.length; i += 2) 
        {
            var t = self.t + Math.floor(i / 2) / self.rate;
            var counter = self.i + Math.floor(i / 2);
            
            var n = this._fn.call(self, t, counter);
            if (isNaN(n)) n = 0;
            self.buffer.writeInt16LE(clamp(signed(n)), i);
        }
        
        self.i += self.buffer.length / 2;
        self.t += self.buffer.length / 2 / self.rate;
        
        self._ticks ++;
        if (!self._ended && self._ticks % 50) this.push(self.buffer);
        else if (!self._ended) process.nextTick(function () { self.push(self.buffer) });
    }
}

var audio_stream = new AudioStream((t,i)=>{return Math.sin(Math.PI*2.0*440.0*t) * 0.1; })
return audio_stream.pipe(process.stdout);
