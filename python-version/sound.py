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
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
        self.synthetizers = []

    def run(self):
        Gst.init(None)
        
        self.time = 0
        self.BYTES_PER_SAMPLE = 4
        self.CHANNELS = 2
        self.SAMPLE_SIZE = self.BYTES_PER_SAMPLE * self.CHANNELS 
        self.RATE = 44100
        self.dt = 1.0 / float(self.RATE)

        gst_string = 'appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=F32LE ! pulsesink'        
        self.player = Gst.parse_launch(gst_string)
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.needdata)
        self.loop = GLib.MainLoop()
        self.loop.run()
        
    def needdata(self, src, length):
        data = bytearray()
        sample_number = int(length / self.SAMPLE_SIZE)        
        for _i in range(0,sample_number):
            value_float = 0.0
            for synthetizer in self.synthetizers:
                value_float = synthetizer.compute(self.time)
                #math.sin(self.time * 2.0 * math.pi * 440.0) * 0.5
            if value_float > 1.0:
                value_float = 1.0
            if value_float < -1.0:
                value_float = -1.0
            value_bytes = struct.pack('f',value_float)            
            for _channel in range(0, self.CHANNELS):
                for byte in value_bytes:
                    data.append(byte)
            self.time += self.dt
            
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

    def shutdown(self):
        self.player.set_state(Gst.State.NULL)
        self.loop.quit()
        self.loop.unref()
    
    def play(self):
        self.player.set_state(Gst.State.PLAYING)        
    
    def pause(self):        
        self.player.set_state(Gst.State.PAUSED)        

