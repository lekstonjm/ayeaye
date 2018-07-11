#!/usr/bin/env python
import threading
import time
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib
import random
import struct
import math

class Sound(threading.Thread):
    def __init__(self, channels = 2, rate = 44100):
        threading.Thread.__init__(self)
        self.BYTES_PER_SAMPLE = 4
        self.CHANNELS = channels
        self.SAMPLE_SIZE = self.BYTES_PER_SAMPLE * self.CHANNELS 
        self.RATE = rate
        self.channels = [None]*self.CHANNELS 
        self.dt = 1.0 / float(self.RATE)
        self.time = 0
        self.started = False
        self.initialize()
    
    def initialize(self):
        Gst.init(None)
        gst_string = 'appsrc name=source ! capsfilter caps=audio/x-raw,rate=%i,channels=%i,format=F32LE ! pulsesink' % (self.RATE, self.CHANNELS)        
        self.player = Gst.parse_launch(gst_string)
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.needdata)

    def run(self):
        self.started = True
        self.loop = GLib.MainLoop()
        self.loop.run()
        
    def needdata(self, src, length):
        data = bytearray()
        sample_number = int(length / self.SAMPLE_SIZE)        
        for _i in range(0,sample_number):
            for _channel in range(0, self.CHANNELS):
                value_float = float(self.channels[_channel](self.time))
                if value_float > 1.0:
                    value_float = 1.0
                if value_float < -1.0:
                    value_float = -1.0
                value_bytes = struct.pack('f',value_float)            
                for byte in value_bytes:
                    data.append(byte)
            self.time += self.dt
            
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

    def shutdown(self):
        self.player.set_state(Gst.State.NULL)
        self.loop.quit()
        self.loop.unref()
    
    def play(self):
        if self.started == False:
            self.start()
        self.player.set_state(Gst.State.PLAYING)        
    
    def pause(self):        
        self.player.set_state(Gst.State.PAUSED)        


if __name__ == "__main__":
    from sys import stdin
    sound = Sound()
    sound.channels[0] = lambda time: math.sin(2.0*440.0*math.pi*time)
    sound.channels[1] = lambda time: math.sin(2.0*330.0*math.pi*time)
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()