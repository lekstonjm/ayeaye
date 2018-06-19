#!/usr/bin/env python
import threading
import time
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib
import random

class Sound(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
	self.start()

    def run(self):
	Gst.init(None)
        gst_string = "appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=S16LE ! pulsesink"
        self.player = Gst.parse_launch(gst_string)
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.needdata)
        self.loop = GLib.MainLoop()
        self.loop.run()
        
    def needdata(self, src, length):
        data = bytearray()
        for i in range(length):
            data.append(random.randint(0, 255))
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

    def shutdown(self):
        self.player.set_state(Gst.State.NULL)
        self.loop.quit()
        self.loop.unref()
    
    def play(self):
        self.player.set_state(Gst.State.PLAYING)        
    
    def pause(self):        
        self.player.set_state(Gst.State.PAUSED)        

