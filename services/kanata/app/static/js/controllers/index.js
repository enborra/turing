angular.module('core_app').controller('IndexController', function IndexController($scope){
    'use strict';
    console.log('Log controller loaded.');

    $('.navbar').removeClass('dark-mode');

    $scope.title = 'loaded.';

    $scope.showSomething = function(){
        this.title = 'clicked! ' + Date();
    };
});
