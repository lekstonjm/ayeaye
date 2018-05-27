var http = require('http');

var synths = {};

var server = http.createServer();

server.on('request', function (req, res) 
{
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader(
        'Access-Control-Allow-Methods',
        'GET, POST, PUT, DELETE, OPTIONS'
    );
    if (req.method === 'OPTIONS') {
        res.end();
    }
});

server.on('request', function(req, res) 
{
    if (req.method === "POST")
    {
        var query_array = req.url.split("/");
        var query = query_array[1];
        var synth_name = "";
        if (query === "s")
        {
            synth_name = query_array[2];
        }
        var data = "";
        req.on('data', function(buf) {data += buf} );
        req.on('end', function()
        {
            console.log(query);
            console.log(synth_name);        
            console.log(data);
        })
    }
    res.end('OK');
});

server.listen(5000);