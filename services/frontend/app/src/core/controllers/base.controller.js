module = angular.module("jupiter.core");
module.controller('BaseController', BaseController);


function BaseController($error, $auth, $user, $scope) {
    $scope.user = $user;
    $scope.auth = $auth;
    $scope.error = $error;
}
