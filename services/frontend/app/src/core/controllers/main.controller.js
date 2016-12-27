module = angular.module("jupiter.core");
module.controller("MainController", MainController);


function MainController($location, $scope) {
    this.redirect = function() {
        if ($scope.user.isAuthenticated()) {
            $location.path("/overview/");
        } else {
            $location.path("/landing/");
        }
    }
}
