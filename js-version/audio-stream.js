'use strict';
var Readable = require('readable-stream').Readable;
var Env = require('./env.js');

const BYTES_PER_SAMPLE = 4;
const CHANNELS_NUMBER = 1;
const DEFAULT_RATE = 44100;
const FALLBACK_BUFFER_SIZE = 4096;
const DEFAULT_BPM = 60;
const BPM_TO_BPS = 1.0/60.0;
const SAMPLE_SIZE = BYTES_PER_SAMPLE*CHANNELS_NUMBER;
const CONTROL_PERIOD = 0.01;


class AudioStream extends Readable
{
    constructor() 
    {
        super();
        this.readable = true;
        this.rate = DEFAULT_RATE;
        this.t = 0;
        this.t_control = 0;
        this.t_beat = 0;
        this.ratio_beat = 0;
        this.bar = 0;
        this._ticks = 0;
        this.buffer = null;
        this.synths = {};
        this.squences = {};
        this.bpm = DEFAULT_BPM;
        this.player = null;
    }
    
    _read(bytes)
    {
        function clamp_one(x) {
            if (x > 1.0) { return 1.0; }
            if (x < -1.0) { return -1.0; }
            return x;
        } 
        function clamp(x) {
            if (x < 0.0) return 0.0;
            if (x > 1.0) return 1.0;
            return x;
        }
        function lin(rel, x_min, x_max) {
            return x_min + (x_max - x_min) * clamp(rel);
        }
        if (!bytes) bytes = FALLBACK_BUFFER_SIZE;
        if (this.buffer === null) 
        {
            this.buffer = new Buffer(Math.floor(bytes));
        }
        //var self = this
        var dt = 1.0/this.rate;
        for (var i = 0; i < this.buffer.length; i += SAMPLE_SIZE) 
        {
            this.t += dt;            
            
            if (this.t_control === 0 || this.t >= this.t_control + CONTROL_PERIOD ) {
                this.t_control = this.t_control + CONTROL_PERIOD;
                for (var synth_name in this.synths)
                {
                    var synth = this.synths[synth_name];
                    if (synth.ended) {
                        delete this.synths[synth_name];
                        continue;
                    }
                    synth.control.call(synth,this.t);                                                
                    for (var item in synth.to_props) {
                        synth.from_props[item] = synth.to_props[item];
                        synth.to_props[item] = synth[item];
                        synth[item] = synth.from_props[item];
                    }                     
                }
            }            
            
            this.t_beat = this.t * this.bpm * BPM_TO_BPS;
            
            var beat = Math.floor(this.t_beat);
            var ratio_beat = this.t_beat - beat;
            if (ratio_beat < this.ratio_beat) {
                this.new_beat = true;
                this.bar ++;
                if (this.bar > 3) {
                    this.bar = 0;
                    this.new_bar = true;
                }                     
            }
            this.ratio_beat = ratio_beat;

            var rel = (this.t - this.t_control)/CONTROL_PERIOD; 
            var val = 0.0;            
            for (var synth_name in this.synths)
            {
                var synth = this.synths[synth_name];
                
                for (var item in synth.to_props) {
                    if (synth.from_props[item] != synth.to_props[item]) {
                        synth[item] = lin(rel, synth.from_props[item],synth.to_props[item]);
                    }
                }
                
                val += synth.generate.call(synth,this.t);
            }                

            if (isNaN(val)) val = 0;
            this.buffer.writeFloatLE(clamp_one(val), i);
        }
        
        //self.i += self.buffer.length / SAMPLE_SIZE;
        //self.t += self.buffer.length / SAMPLE_SIZE / self.rate;
        
        this._ticks ++;
        var self = this;
        if (!this._ended && this._ticks % 50) this.push(this.buffer);        
        else if (!this._ended) process.nextTick(function () { self.push(self.buffer) });    
    }
}

module.exports = AudioStream;