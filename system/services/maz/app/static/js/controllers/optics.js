angular.module('core_app').controller('OpticController', function OpticController($scope){
    'use strict';
    console.log('OpticController loaded.');

    $scope.title = 'loaded.';

    $('.navbar').addClass('dark-mode');

    $scope.showSomething = function(){
        this.title = 'clicked! ' + Date();
    };
});
