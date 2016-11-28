angular.module('core_app').controller('LogController', function LogController($scope, grand_central_service){
    'use strict';

    // $scope.gcs = grand_central_service.receive_pipeline_msg();

    $scope.logs = grand_central_service.logs;

    console.log('Log controller loaded.');
    console.log('Number of log records in global gcs service: ' + $scope.logs.length);

    $('.navbar').removeClass('dark-mode');

    $scope.channel = '/system';
    $scope.msg = '{"sender": "harness", "type": "warning", "message": "Testing harness."}';

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

    $scope.publish_msg = function(){
        client.publish($scope.channel, $scope.msg);
    };
});
