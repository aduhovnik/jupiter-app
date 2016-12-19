module = angular.module("jupiter.core");
module.controller('BaseController', BaseController);


function BaseController($error) {
    $error.onSuccess();
    this.getError = $error.getError;
}