class Clock():
    def __init__(self, bpm =60.0, time_signature = 4.0/4.0, rate=44100):
        self.bpm = bpm
        self.time_signature = time_signature
        self.rate = rate
        self.dt = 1.0/float(rate)
        self.beat_period = 60.0 / self.bpm
        self.bar_period = self.time_signature * self.beat_period * 4.0
        self.reset()
    def tick(self):
        self.time += self.dt
        self.new_beat = False
        self.new_bar = False
        self.beat = (self.next_beat_time - self.time)/self.beat_period 
        self.bar = (self.next_bar_time - self.time)/self.bar_period
        if self.time > self.next_beat_time:
            self.next_beat_time = self.next_beat_time + self.beat_period
            self.new_beat = True
        if self.time > self.next_bar_time:
            self.next_bar_time = self.next_bar_time + self.bar_period
            self.new_bar = True
    def reset(self):
        self.time = 0.0 
        self.bar = 0.0
        self.beat = 0.0
        self.new_beat = True
        self.new_bar = True
        self.next_beat_time = 0.0
        self.next_bar_time = 0.0
        self.next_beat_time = self.next_beat_time + 60.0/self.bpm
    def __str__(self):
        return "time=%f, beat=%f, bar=%f, new beat=%i, new bar=%i" % (self.time, self.beat, self.bar, self.new_beat, self.new_bar)

if __name__ == "__main__":
    clock = Clock()
    for i in range(0,10000):
        if clock.new_beat or clock.new_bar:
            print clock
        clock.tick()
