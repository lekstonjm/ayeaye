function SynthDef(name, default_props, generator, controller) {
    this.name = name;
    this.props = default_props;
    if (typeof(generator) === "function") {
        this.generator = generator;
    } else {
        eval('this.generator = '+generator);
    }
    if (typeof(controller) === "function") {
        this.controller = controller;
    } else {
        eval('this.controller = '+controller);
    }                
}

SynthDef.prototype.create = function(t,instance_props, name)
{
    function Synth(name, t, props, generator, controller)
    {
        this.name = name;
        this.t0 = t;
        
        this.from_props = {};
        this.to_props = {};
        
        for(var item in props)
        {
            this[item] = props[item];
            
            this.from_props[item] = this[item];
            this.to_props[item] = this[item];
            
        }
        this.generator = generator;
        this.controller = controller;
        this.ended = false;
        this.enabled = true;
    }

    Synth.prototype.generate = function(t) {  
        return (this.enabled && this.generator !== undefined)?this.generator.call(this,this,t):0.0; 
    }

    Synth.prototype.control = function(t) { 
        if (this.controller !== undefined)
        {
            this.controller.call(this,this,t);
        }    
    }

    var synth_name = "";
    if (name !== undefined) {
        synth_name = name;
    } else {
        if (this.autoname_count === undefined) this.autoname_count = 0;
        synth_name = "_default_synthname_"+this.autoname_count;
        this.autoname_count = this.autoname_count+1;
    }

    var synth = new Synth(synth_name, t,  this.props, this.generator, this.controller);

    if (instance_props !== undefined)
    {
        for (var item in instance_props)
        {
            if (synth[item] !== undefined) 
            {
                synth[item] = instance_props[item];
                
                synth.from_props[item] = synth[item];
                synth.to_props[item] = synth[item];
                
            }
        }
    }
    if (synth.control !== undefined) {
        synth.control.call(synth, t);
    }
    for (var item in synth.to_props) {
        synth.from_props[item] = synth[item];
        synth.to_props[item] = synth[item];
    }

    return synth;    
}

module.exports = SynthDef;
