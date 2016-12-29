module = angular.module("jupiter.core");
module.controller("MainController", MainController);


function MainController($location, $scope) {
    this.redirect = function() {
        var path;
        if ($scope.user.isAuthenticated()) {
            path = $scope.user.isAdmin() ? "/clients/" : "/clients/me";
            $location.path("/overview/");
        } else {
            path = "/landing/";
        }
        $location.path(path);
    }
}
