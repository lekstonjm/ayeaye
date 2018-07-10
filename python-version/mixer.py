from value_state import ValueState

class Mixer():
    def __init__(self):
        self.voices = []
    def __call__(self,time):
        value = ValueState(0.0, False)
        weight = 0.0
        for voice in self.voices:
            weight += voice[0]
            value = value + voice[1](time)
        if weight > 0.0:
            value /= weight
        return value
if __name__ == "__main__":
    from sys import stdin
    from sound import Sound
    from sinosc import SinOsc
    mixer = Mixer()
    mixer.voices.append([0.5, SinOsc(440.0)])
    mixer.voices.append([0.5, SinOsc(330.0)])
    sound = Sound()
    sound.generator = mixer
    sound.start()
    sound.play()
    stdin.readline()
    sound.shutdown()
