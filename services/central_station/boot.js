var mosca = require('mosca');


var server = new mosca.Server({
  port: 1883
});


server.on('ready', setup);
server.on('published', recieve);


function recieve(packet, client){
  console.log( 'Published', packet.payload.toString() );
}

function setup(){
  console.log( 'Mosca server is up and running.' );
}
