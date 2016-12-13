angular.module('core_app').controller('MachineController', function MachineController($scope){
    'use strict';

    console.log('Machine controller loaded.');

    $('.navbar').removeClass('dark-mode');

    $scope.title = 'loaded.';
});
