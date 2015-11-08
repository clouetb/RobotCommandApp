var static = require('node-static');
var http = require('https');
var fs = require('fs')

var options = {
  key: fs.readFileSync('server.key'),
  cert: fs.readFileSync('server.crt')
};

var file = new(static.Server)();
var app = http.createServer(options, function (req, res) {
  file.serve(req, res);
}).listen(2013);
