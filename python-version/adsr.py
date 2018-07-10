
from value_state import ValueState 
import composer
class ADRS():
    def __init__(self, t0 = 0.0, a=0.04, d=0.1, s = 0.1, r = 0.1, dl = 0.6):
        self.t0 = t0
        self.a = a
        self.d = d
        self.s = s
        self.r = r 
        self.dl = dl
    def __call__(self, time):
        value = 0.0
        ended = False
        duration = time - self.t0
        if duration  > self.a + self.d + self.s + self.r:
            ended = True
        elif self.r > 0.0 and duration > self.a + self.d + self.s:
            d = duration - (self.a + self.d + self.s)
            value =  self.dl * (1.0 - d / self.r)
        elif self.s > 0.0 and duration > self.a + self.d:
            value = self.dl
        elif self.d > 0.0 and duration > self.a:
            d = duration - self.a
            value = 1.0 + (self.dl - 1.0) * d / self.d   
        elif self.a > 0.0 and duration > 0.0:
            d = duration
            value = d / self.a            
        return ValueState(value, ended)

class ADRSFactory(composer.ComposerFactory):
    def __init__(self, params = None):
        self.params = params
        composer.ComposerFactory.__init__(self,self)
    def __call__(self, time, params = None):
        adsr = ADRS(time)
        if self.params is not None:
            for key in self.params:
                if key in adsr.__dict__:
                    setattr(adsr, key, self.params[key])            
        if params is not None:
            for key in params:
                if key in adsr.__dict__:
                    setattr(adsr, key, params[key])
        return adsr

if __name__ == "__main__":
    from sys import stdin
    from sound import Sound
    from sinosc import SinOscFactory
    osc = SinOscFactory()
    adsr = ADRSFactory()
    factory = osc*adsr
    generator = factory(0.0)
    sound = Sound()
    sound.generator = generator
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()