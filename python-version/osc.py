from value_state import ValueState
from composer import Composer

class Osc():
    def __init__(self, gen = None, params = None):
        self.gen = gen
        self.params = params
    def __call__(self, time):
        return ValueState(self.gen(time, self.params), False)
        
class OscDef(Composer):
    def __init__(self, gen,  params = None):
        Composer.__init__(self,self)
        self.gen = gen
        self.params = params
    def __call__(self, time = 0.0, params = None):
        osc_params = {}
        if self.params is not None:
            for key in self.params:
                osc_params[key] = self.params[key]
        if params is not None:
            for key in params:
                osc_params[key] = params[key]
        osc = Osc(self.gen, osc_params)
        return osc

if __name__ == "__main__":
    from sys import stdin
    from sound import Sound
    import math
    osc_def = OscDef(lambda t,p:math.sin(2.0*math.pi*p["freq"]*t)*p["amp"], {"freq":440.0, "amp":1.0})
    sound = Sound(1) 
    osc = osc_def(0.0, {"freq" : 440.0})
    sound.channels[0] = osc
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()