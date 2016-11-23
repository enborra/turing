var core_app = angular.module('core_app', [
    'ngRoute'
]);

core_app.config(function( $routeProvider, $locationProvider ){
    'use strict';

    $locationProvider.html5Mode(true);

    $routeProvider.when('/', {
        templateUrl: '/static/views/index.htm',
        controller: 'IndexController'
    })

    .when('/logs', {
        templateUrl: '/static/views/logs.htm',
        controller: 'LogController'
    })

    .when('/machine', {
        templateUrl: '/static/views/machine.htm',
        controller: 'MachineController'
    })

    .when('/optics', {
        templateUrl: '/static/views/optics.htm',
        controller: 'OpticController'
    });
});






core_app.service('grand_central_service', function($rootScope){
    var self = this;
    this.logs = [];

    // this.receive_pipeline_msg = function(){
    //     this.logs.push({id:10});
    //
    //     return this.logs.length;
    // };

    this.add_log_entry = function(msg_obj){
        // TODO: needs object validation for log item

        var new_log = {
            id: self.logs.length,
            title: msg_obj['title'],
            description: msg_obj['description'],
            timestamp: msg_obj['timestamp'],
            topic: msg_obj['topic']
        };

        self.logs.push(new_log);

        console.log('Added new log entry. total log collection size is ' + this.logs.length.toString());
    };



    var port = 3000;
    var host = 'localhost';
    var options = {
        // host: host,
        // port: port,
        // clientId: 'Browser' + new Date().getTime(),
        // reconnectPeriod: 1000
    };



    /*  If an anchor or the logo in navigation are clicked,
        hide the nav menu */

    $('.nav a, .navbar-brand').on('click', function(){
        $('.btn-navbar').click(); //bootstrap 2.x
        $('.navbar-collapse').collapse('hide') //bootstrap 3.x by Richard
    });

    /*  If the nav logo is clicked, remove section highlights. */

    $('.navbar-brand').on('click', function(){
        $('.nav a').removeClass('highlight');
    });

    /* If a section anchor is clicked, highlight that section. */

    $('.nav a').on('click', function(e){
        $('.nav a').removeClass('highlight');

        $(e.target).addClass('highlight');
    });

    this.handleConnect = function(){
        console.log('Connected');
        client.subscribe('/system');
        client.subscribe('/system/face');

        $('.blinker').addClass('connected');
    };

    this.handleClose = function(){
        console.log('Closed, reconnecting in '+ options.reconnectPeriod);

        $('.blinker').removeClass('connected');
    };

    this.handleMessage = function(topic, message){
        // console.log('Received:', topic, 'Message:', message);

        // document.write('Received message: ' + message);
        // document.write('<br/>');

        // $('tbody').append('<tr><td>'+Date().toString()+'</td><td>'+message+'</td></tr>');

        if( message.length > 20 ){
            $('#display-photo').attr('src', 'data:image/jpeg;base64,'+message)
        }

        if( topic == '/system' ){
            self.add_log_entry({
                topic: topic,
                description: message,
                timestamp: Date.now()
            });

            $rootScope.$apply();
        }
    };

    console.log('Connecting...');

    client = mqtt.connect('mqtt://'+window.location.host, {
        port: port
    });

    client.on('connect', this.handleConnect);
    client.on('message', this.handleMessage);
    client.on('close'  , this.handleClose);

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
