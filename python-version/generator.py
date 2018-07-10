class Generator():
    def __init__(self, definition = None, sequences = None):
        self.voices = []
        self.definition = definition
        if self.definition is None:
            self.definition = []
        self.sequences = sequences
        if self.sequences is None:
            self.sequences = []
        self.index = 0
        self.next_time = -1.0
    def __call__(self, time):
        if len(self.sequences) > 0:
            if self.next_time < 0.0 or time > self.next_time: 
                self.next_time = time + self.sequences[self.index]["l"]
                self.voices.append(self.definition(time,self.sequences[self.index]["p"]))
                self.index += 1
                if self.index >= len(self.sequences):
                    self.index = 0
        weight = 0.0
        total = 0.0
        for voice in self.voices:
            value_state = voice(time)
            total += float(value_state)
            if value_state:
                self.voices.remove(voice)
        if weight > 0.0:
            return total/weight
        return total    
        
if __name__ == "__main__":
    from sys import stdin
    from sound import Sound
    from sinosc import SinOscFactory
    from adsr import ADRSFactory
    osc = SinOscFactory()
    adsr = ADRSFactory({"a":0.01, "d":0.0, "s":0.0, "r":0.1, "dl":1.0})    
    sound = Sound() 
    generator = Generator(osc*adsr, [{"l":0.25,"p":{"freq":440.0}}, {"l":0.25,"p":{"freq":330.0}}])
    sound.generator = generator
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()