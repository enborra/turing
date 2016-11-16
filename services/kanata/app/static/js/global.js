$(document).ready(function(){

    var port = 3000;
    var host = 'localhost';
    var options = {
        // host: host,
        // port: port,
        // clientId: 'Browser' + new Date().getTime(),
        // reconnectPeriod: 1000
    };

    var handleConnect = function(){
        console.log('Connected');
        client.subscribe('/system/face');
    }

    var handleClose = function(){
        console.log('Closed, reconnecting in '+ options.reconnectPeriod);
    }

    var handleMessage = function(topic, message){
        console.log('Received:', topic, 'Message:', message);

        // document.write('Received message: ' + message);
        // document.write('<br/>');

        // $('tbody').append('<tr><td>'+Date().toString()+'</td><td>'+message+'</td></tr>');

        if( message.length > 20 ){
            $('#display-photo').attr('src', 'data:image/jpeg;base64,'+message)
        }
    }

    console.log('Connecting...');

    var client = mqtt.connect('mqtt://'+window.location.host, {
        port: port
    });

    client.on('connect', handleConnect);
    client.on('message', handleMessage);
    client.on('close'  , handleClose);

    var heartbeatCount = 0;
    // var heartbeatTimer = setInterval(function(){
    //     heartbeatCount++;
    //
    //     var topic = '/system';
    //
    //     client.publish(topic, 'hrm');
    //     console.log('Published', topic);
    // }, 1000);

});
