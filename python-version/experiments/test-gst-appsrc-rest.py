#!/usr/bin/env python
import gi
gi.require_version("Gst","1.0")
from gi.repository import Gst
import random
import web

class Sound:
    def __init__(self):
        self.player = Gst.parse_launch('appsrc name=source ! capsfilter caps=audio/x-raw,rate=44100,channels=2,format=S16LE ! pulsesink')
        playersrc = self.player.get_by_name('source')
        playersrc.connect('need-data', self.need_data)

    def start(self):
        self.player.set_state(Gst.State.PLAYING)

    def stop(self):
        self.player.set_state(Gst.State.PAUSED)

    def need_data(self, src, length):
        print 'need data:', length
        data = bytearray()
        for i in range(length):
            data.append(random.randint(0, 255))
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