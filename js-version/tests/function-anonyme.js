var titi = [];
var toto = [];
titi[0] = (() => 
{
    function toto()
    {
        this.freq = 440;
    }
    toto.prototype.hi = function(t)
    {
        return Math.sin( Math.PI * 2.0 * this.freq * t);
    }    
    toto.prototype.lo = function(t) 
    {

    }
    return new toto();
}
)();

titi[1] = (()=>
{
    class toto 
    {
        constructor() { this.freq = 440;}
        compute(t) { return Math.sin( Math.PI * 2.0 * this.freq * t); }
    }
    return new toto;
})();


function SynthDef(props, fn)
{
    this.props = props;
    this.fn = fn;
}
SynthDef.prototype.create = function()
{
    function Synth(props, fn)
    {
        for(var item in props)
        {
            this[item] = props[item];
        }
        this.fn = fn;
    }

    Synth.prototype.compute = function(t) { return this.fn.call(null,this,t); }
    return new Synth(this.props, this.fn);    
}

var synthdef = new SynthDef({'freq':440}, (o,t) => {return Math.sin( Math.PI * 2.0 * o.freq * t);})

var synth = synthdef.create();
console.log(synth);


console.log(titi[0].hi(0));
console.log(titi[1].compute(0.25/440.0));
titi[1].freq = 550.0;
console.log(titi[1].compute(0.25/440.0));
titi[2] = {freq:440.0, compute:function(t) {return Math.sin( Math.PI * 2.0 * this.freq * t);}};
console.log(titi[2].compute(0.25/440.0));
titi[2].freq = 550.0;
console.log(titi[2].compute(0.25/440.0));
titi[3] = synthdef.create();
console.log(titi[3].compute(0.25/440.0));


var synthdefs = {};
synthdefs['sin'] = new SynthDef({'freq':440},(o,t)=>{return Math.cos( Math.PI * 2.0 * o.freq * t);});
var synths = {};
synths['A'] = synthdefs['sin'].create();
console.log(synths['A'].compute(0.25/440.0));
