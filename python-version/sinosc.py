import math
from value_state import ValueState
import composer

class SinOsc(composer.ComposerFactory):
    def __init__(self, freq = 440.0, amp = 1.0):
        self.freq = freq
        self.amp = amp
    def __call__(self, time):
        return ValueState(math.sin(2.0*math.pi*self.freq*time)*self.amp, False)
        
class SinOscFactory(composer.ComposerFactory):
    def __init__(self, params = None):
        composer.ComposerFactory.__init__(self,self)
        self.params = params
    def __call__(self, time = 0.0, params = None):
        sinosc = SinOsc()
        if self.params is not None:
            for key in self.params:
                if key in sinosc.__dict__:
                    setattr(sinosc, key, self.params[key])                    
        if params is not None:
            for key in params:
                if key in sinosc.__dict__:
                    setattr(sinosc, key, params[key])
        return sinosc

if __name__ == "__main__":
    from sys import stdin
    from sound import Sound
    factory = SinOscFactory()
    sound = Sound() 
    sound.generator = factory(0.0, {"freq" : 220.0})
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()