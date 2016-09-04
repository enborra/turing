var mosca = require('mosca');

var pubsubsettings = {

}

var moscaSettings = {
  port: 1883,
  backend: pubsubsettings
};

var server = new mosca.Server(moscaSettings);
server.on('ready', setup);

function setup(){
  console.log( 'Mosca server is up and running.' );
}
