#!/usr/bin/env python
import pygst
pygst.require("0.10")
import gst, gtk
import random
import gobject
gobject.threads_init()

class Sound:
     def __init__(self):
         self.player = gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw-int,rate=44100,channels=2,depth=16,signed=true ! pulsesink')
         playersrc = self.player.get_by_name('source')
         playersrc.connect('need-data', self.needdata)
         self.player.set_state(gst.STATE_PLAYING)
         gtk.main()

     def needdata(self, src, length):
         print 'need-data:', length
         data = ''
         for i in range(length):
             data = data + chr(random.randint(0, 255))
         src.emit('push-buffer', gst.Buffer(data))

sa = Sound() 