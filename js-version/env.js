Env = {}
Env.Perc = function(t, attack_duration, attack_level, release_duration) {
    if (attack_duration === undefined) { attack_duration = 0.1;}
    if (attack_level === undefined) { attack_level = 1.0;}
    if (release_duration === undefined) { release_duration = 0.3; }
    var value = 0.0;
    var ended = false;
    if (t < attack_duration) {
        value = attack_level * t / attack_duration;
    }
    else if (t < attack_duration+release_duration) {
        value = attack_level - ( t - attack_duration) * attack_level / release_duration; 
    } else {
        ended = true;
    }
    return {'value' : value, 'ended' : ended};
}
Env.ADSR = function(t, attack_duration, attack_level, decay_duration, decay_level, sustain_duration, release_duration) {
    if (attack_duration === undefined) { attack_duration = 0.3;}
    if (attack_level === undefined) { attack_level = 1.0;}
    if (decay_duration === undefined) { release_duration = 0.1; }
    if (decay_level === undefined) { release_duration = 0.7; }
    if (sustain_duration === undefined) { release_duration = 1.0; }
    if (release_duration === undefined) { release_duration = 0.1; }
    var value = 0.0;
    var ended = false;    
    if (t < attack_duration) {
        value = attack_level * t / attack_duration;
    } else if (t < attack_duration+decay_duration) {
        value = attack_level - (t - attack_duration) (decay_level - attack_level) / decay_duration;  
    } else if (t < attack_duration + decay_duration + sustain_duration) {
        value = decay_level;
    } else if ( t < attack_duration + decay_duration + sustain_duration + release_duration) {
        value = decay_level - ( t - (attack_duration + decay_duration + sustain_duration) ) * decay_level / release_duration; 
    } else {
        ended = true;
    }
    return {'value' : value, 'ended' : ended};
}

module.exports = Env;