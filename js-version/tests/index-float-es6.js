'use strict';
var Readable = require('readable-stream').Readable;
var Spawn = require('child_process').spawn;

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
        this.beat = 0;
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
        function clamp_one(x)
        {
            if (x > 1.0) { return 1.0; }
            if (x < -1.0) { return -1.0; }
            return x;
        } 
        if (!bytes) bytes = 4096;
        if (this.buffer === null) 
        {
            this.buffer = new Buffer(Math.floor(bytes)); 
        }
        var self = this;
                
        for (var i = 0; i < self.buffer.length; i += 4) 
        {
            var t = self.t + Math.floor(i / 4) / self.rate;
            var counter = self.i + Math.floor(i / 4);
            
            var n = this._fn.call(self, t, counter);
            if (isNaN(n)) n = 0;
            self.buffer.writeFloatLE(clamp_one(n), i);
        }
        
        self.i += self.buffer.length / 4;
        self.t += self.buffer.length / 4 / self.rate;
        while (self.t > self.beat + 1.0)  {
            self.beat = self.beat + 1.0;
            console.warn("beat : "+self.beat);
        }
        self._ticks ++;
        if (!self._ended && self._ticks % 50) this.push(self.buffer);
        else if (!self._ended) process.nextTick(function () { self.push(self.buffer) });
    }
}

var audio_stream = new AudioStream((t,i)=>{return Math.sin(Math.PI*2.0 * 110.0*t)*0.1;})

var player = Spawn("play", ["-c","1","-r","44100","-t","f32", "--ignore-length", "-"]);
player.on('error', function(err) { console.error(err); });
player.stdin.on('error', function(err) { console.error(err);});

return audio_stream.pipe(player.stdin)

//return audio_stream.pipe(process.stdout);
