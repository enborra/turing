angular.module('core_app').controller('LogController', function LogController($scope, grand_central_service){
    'use strict';

    // $scope.gcs = grand_central_service.receive_pipeline_msg();

    $scope.logs = grand_central_service.logs;

    console.log('Log controller loaded.');
    console.log('Number of log records in global gcs service: ' + $scope.logs.length);

    $('.navbar').removeClass('dark-mode');

    setInterval(function(){
        $scope.$apply();
    }, 5000);

    $scope.computeTime = function(time_obj){
        var resp = null;
        var minutes_delta = 0;

        minutes_delta = ((Date.now()-time_obj)/(1000*60));

        if( minutes_delta < 0.25 ){
            resp = 'Just now';
        } else if( minutes_delta < 1 ){
            resp = '< 1 min ago.';
        } else if( minutes_delta < 60 ){
            resp = Math.round(minutes_delta) + ' min ago';
        } else if( minutes_delta < 1440 ){
            resp = 'more than an hour ago.';
        } else {
            resp = 'a long time ago, in a galaxy far, far away.';
        }

        return resp;
    };

    $scope.msg_template_items = [
        {
            'value': 'logging_info',
            'category': 'logging',
            'channel': '/system',
            'label': 'Logging: Standard info log message',
            'obj': {
                'sender': 'harness',
                'type': 'info',
                'msg': 'Something clever.'
            }
        },
        {
            'value': 'logging_warning',
            'category': 'logging',
            'channel': '/system',
            'label': 'Logging: Standard warning log message',
            'obj': {
                'sender': 'harness',
                'type': 'warning',
                'msg': 'Something concerning.'
            }
        },
        {
            'value': 'logging_error',
            'category': 'logging',
            'channel': '/system',
            'label': 'Logging: Standard error log message',
            'obj': {
                'sender': 'harness',
                'type': 'error',
                'msg': 'Something alarming.'
            }
        },
        {
            'value': 'learn_face',
            'category': 'optics',
            'channel': '/optics',
            'label': 'Optics: Trigger learn of any face currently in camera view',
            'obj': {
                'sender': 'harness',
                'type': 'action',
                'msg': 'learn_face'
            }
        },
        {
            'value': 'retrain_faces',
            'category': 'optics',
            'channel': '/optics',
            'label': 'Optics: Trigger full retrain of library',
            'obj': {
                'sender': 'harness',
                'type': 'action',
                'msg': 'retrain_faces'
            }
        }
    ];

    $scope.on_msg_template_change = function(){
        console.log('Changed: ' + $scope.selectedItem.label);

        $scope.channel = $scope.selectedItem.channel;
        $scope.msg = JSON.stringify($scope.selectedItem.obj, undefined, 4);
    };

    $scope.publish_msg = function(){
        console.log('Publishing message to GrandCentral.');
        
        client.publish($scope.channel, $scope.msg);
    };
});
