class ValueState():
    def __init__(self, value, ended):
        self.value = value
        self.ended = ended
    def __float__(self):
        return self.value
    def __bool__(self):
        return self.ended
    def __nonzero__(self):
        return self.__bool__()
    def __add__(self, other):
        if isinstance(other, ValueState):
            return ValueState(self.value + other.value, self.ended or other.ended)
        return ValueState(self.value - other, self.ended)
    def __sub__(self, other):
        if isinstance(other, ValueState):
            return ValueState(self.value - other.value, self.ended or other.ended)
        return ValueState(self.value - other, self.ended)
    def __mul__(self, other):
        if isinstance(other, ValueState):
            return ValueState(self.value * other.value, self.ended or other.ended)
        return ValueState(self.value * other, self.ended)    
    def __div__(self, other):
        if isinstance(other, ValueState):
            return ValueState(self.value / other.value, self.ended or other.ended)
        return ValueState(self.value / other, self.ended)
    def __str__(self):
        return "{value:%d,ended:%i}" % (self.value, self.ended)
