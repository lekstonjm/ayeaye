class Composer():
    def __init__(self, source):
        self.source = source
    def __mul__(self, other):
        if isinstance(other, Composer):
            return ComposerMul(self, other)
        else:
            return ComposerMul(self,Composer(other))
    def __call__(self, time = 0.0, params = None):
        if isinstance(self.source, float):
            return lambda time: self.source 
        return self.source(time, params)

class ComposerMul(Composer):
    def __init__(self, factor1, factor2):
        self.factor1 = factor1
        self.factor2 = factor2 
    def __call__(self, time = 0, params = None):
        composer1 = self.factor1(time, params)
        composer2 = self.factor2(time, params)        
        return lambda time: composer1(time)*composer2(time) 



if __name__ == "__main__":
    import adsr
    import sinosc
    c1 = sinosc.SinOscDef()
    c2 = adsr.ADRSDef()
    c3 = c1 * c2 * 3.0
    o = c3(0.0)
    print float(o(0.05))