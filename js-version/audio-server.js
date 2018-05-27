var Express = require('express');
var SynthDef = require('./synthdef.js');
var AudioStream = require('./audio-stream.js');
var Env = require('./env.js');

var app = Express();

var synthdefs = {};
var audio_stream = new AudioStream();
audio_stream.pipe(process.stdout);

app.get('/synthdefs', function(req, res) {
    res.end(JSON.stringify(synthdefs));
});

app.post('/synthdefs/add', function(req,res) {
    var str = '';
    req.on('data', function(chunk) {
        str += chunk;
    });
    req.on('end', function() {
        var data = JSON.parse(str);
        var synthdef = new SynthDef(data["name"],data["props"], data["generator"], data["controller"]);
        synthdefs[synthdef.name] = synthdef;
        console.warn("New synthdef added");
        console.warn(synthdef);
        res.end("ok");    
    });
});

app.post('/synthdefs/remove', function(req,res) {
    var str = '';
    req.on('data', function(chunk) {
        str += chunk;
    });
    req.on('end', function() {
        var data = JSON.parse(str);
        var name = data["name"];
        if (synthdefs[name] !== undefined )
        {
            delete synthdefs[name];
        }
        console.warn("Synthdef removed");
        console.warn(synthdef);
        res.end("ok");
    });
});

app.get('/synths', function(req,res) {
    res.end(JSON.stringify(audio_stream.synths));
});

app.post('/synths/create', function(req,res)
{
    var str = '';
    req.on('data', function(chunk) {
        str += chunk;
    });
    req.on('end', function() {
        var data = JSON.parse(str);
        var synth_name = data["name"];
        var synthdef_name = data["synthdef"];
        var synthdef = synthdefs[synthdef_name];
        if (synthdef !== undefined)
        {
            var synth = synthdef.create(audio_stream.t, data["props"], synth_name);
            audio_stream.synths[synth.name] = synth;
            console.warn("New synth created");
            console.warn(synth);        
        }
        res.end("ok");
    });
});

app.post('/synths/clear', function(req, res)
{
    var str = '';
    req.on('data', function(chunk) {
        str += chunk;
    });
    req.on('end', function() {
        audio_stream.synths = {};
        console.warn("Synths cleared");
        console.warn(audio_stream.synths);        
    res.end("ok");
    });
});

var server = app.listen(5000, function () {

  var host = server.address().address
  var port = server.address().port

  console.warn("Audio server listening at http://%s:%s", host, port)
});