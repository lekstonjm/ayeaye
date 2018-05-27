#!/usr/bin/env python
import gi
gi.require_version("Gst","1.0")
gi.require_version("Gtk","3.0")
from gi.repository import Gst,Gtk
import random


class Sound:
     def __init__(self):
         self.player = Gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=S16LE ! pulsesink')
         playersrc = self.player.get_by_name('source')
         playersrc.connect('need-data', self.needdata)
         self.player.set_state(Gst.State.PLAYING)
         Gtk.main()

     def needdata(self, src, length):
         print 'need-data:', length
         data = bytearray()
         for i in range(length):
             data.append(random.randint(0, 255))
         src.emit('push-buffer', Gst.Buffer.new_wrapped(data))
Gst.init(None)
sa = Sound() 