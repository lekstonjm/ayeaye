# ayeaye
## Introduction
ayeaye is electronic music livecoding plateforme, based on the baudio/baudio-party and is inspired by supercollider and sonic-pi. It's a client/server REST application. It is in a very early development stage.


## Installation
* Works on linux derived plateform. Should probably works on windows without garanty.
* Require sox tools found at http://sox.sourceforge.net/
```
npm install
```
## Start server
```
npm start
```
## Send request
One can use curl to send GET/POST. Personaly, I prefer use Insomnia.
### Add a synthetizer definition
http://localhost:5000/synthdefs/add

__example__ 

Create a basic sinus oscillator sythetizer using a simple percusiv enveloppe

```
{
	"name":"sin",
	"props":{"freq":440.0, "amp":0.1},
	"generator": "(o,t)=>{return Math.sin( Math.PI * 2.0 * o.freq * t) * o.amp}",
	"controller":"(o,t)=>{ var dt = t-o.t0; var env = Env.Perc(dt, 0.1, 0.5, 0.3); o.amp = 0.1 * env.value; o.ended = env.ended;}"
}
```

### Create a synthetizer based on a definition
http://localhost:5000/synths/create

__example__

Create an instance of the sin osc with a frequency as of 330 herz 
{
	"synthdef":"sin",
	"props" : { "freq" : 330 }
}

