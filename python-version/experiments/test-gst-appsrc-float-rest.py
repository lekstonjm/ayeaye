#!/usr/bin/env python
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst
import random
import web
import math
import struct

safe_list = ['math','acos', 'asin', 'atan', 'atan2', 'ceil', 'cos', 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor', 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10', 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt', 'tan', 'tanh']
safe_dict = dict([ (k, locals().get(k, None)) for k in safe_list ])
safe_dict['abs'] = abs


class Sound:
    def __init__(self):
        #self.player = Gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=S16LE ! pulsesink')
        self.player = Gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=F32LE ! pulsesink')
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.need_data)
        self.time = 0
        #self.BYTES_PER_SAMPLE = 2
        self.BYTES_PER_SAMPLE = 4
        self.CHANNELS = 2
        self.SAMPLE_SIZE = self.BYTES_PER_SAMPLE * self.CHANNELS 
        self.RATE = 44100
        self.dt = 1.0 / float(self.RATE)

    def start(self):
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.PAUSED)

    def need_data(self, src, length):
        sample_number = int(length / self.SAMPLE_SIZE)
        data = bytearray()
        for i in range(0,sample_number):
            #value_float_r = random.uniform(-1.0,1.0)
            value_float = math.sin(self.time * 2.0 * math.pi * 440.0) * 0.5
            if value_float > 1.0:
                value_float = 1.0
            if value_float < -1.0:
                value_float = -1.0

            #value_short = int(value_float * 32767.0)

            #value_bytes = struct.pack('h',value_short)
            value_bytes = struct.pack('f',value_float)            
            for byte in value_bytes:
                data.append(byte)
            #value_float_l = 0 
            #value_bytes = struct.pack('f',value_float_l)            
            for byte in value_bytes:
                data.append(byte)
            self.time += self.dt
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

Gst.init(None)
sa = Sound() 
urls = (
    '/start','Start',
    '/stop','Stop'
)

app = web.application(urls, globals())

sound = Sound()

class Start:
    def GET(self):
        sound.start()
        return "{response:ok}"

class Stop:
    def GET(self):
        sound.stop()
        return "{response:ok}"


if __name__ == "__main__":
    app.run()