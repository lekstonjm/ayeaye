#!/usr/bin/env python
import threading
import time
import math
import struct
import gi

gi.require_version("Gst","1.0")
from gi.repository import Gst, GLib

class SoundPlayer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)        
        Gst.init(None)
        gst_string = "appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=F32LE ! alsasink"
        self.player = Gst.parse_launch(gst_string)
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.need_data)
        self.time = 0
        self.BYTES_PER_SAMPLE = 4
        self.CHANNELS = 2
        self.SAMPLE_SIZE = self.BYTES_PER_SAMPLE * self.CHANNELS 
        self.RATE = 44100
        self.dt = 1.0 / float(self.RATE)
        self.is_playing = False
        #bus = self.player.get_bus()
        #bus.add_signal_watch()
        #bus.connect("message", self.handle_gst_message)
        #self.end_of_play_event = threading.Event(True)
        #self.end_of_play_handle = None

    def run(self):
        self.loop = GLib.MainLoop()
        self.loop.run()
        print "end of SoundPlayer thread"
    
    #def handle_gst_message(self, bus, message):
    #    print message.type
    #    if message.type == Gst.MessageType.EOS or message.type == Gst.MessageType.ERROR:
    #        self.player.set_state(Gst.State.NULL)
    #        if self.end_of_play_handle != None:
    #            self.end_of_play_handle()
    #            self.end_of_play_handle = None
    #        self.end_of_play_event.set()

    def need_data(self, src, length):
        sample_number = int(length / self.SAMPLE_SIZE)
        data = bytearray()
        for i in range(0,sample_number):
            value_float = math.sin(self.time * 2.0 * math.pi * 440.0) * 0.5
            if value_float > 1.0:
                value_float = 1.0
            if value_float < -1.0:
                value_float = -1.0

            value_bytes = struct.pack('f',value_float)            
            for byte in value_bytes:
                data.append(byte)

            for byte in value_bytes:
                data.append(byte)
            self.time += self.dt
        src.emit('push-buffer', Gst.Buffer.new_wrapped(data))

    def play(self):
        self.player.set_state(Gst.State.PLAYING)
        self.is_playing = True


    def pause(self):
        self.player.set_state(Gst.State.PAUSED)
        self.is_playing = False        
         
    def is_playing(self):
        return self.is_playing
    
    def shutdown(self):
        self.loop.quit()
        self.loop.unref()


if __name__ == "__main__":
    soundPlayer = SoundPlayer()
    soundPlayer.start()
    soundPlayer.play()
    soundPlayer.shutdown()
