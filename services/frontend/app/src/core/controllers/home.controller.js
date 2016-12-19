module = angular.module("jupiter.core");
module.controller('HomeController', HomeController);


function HomeController($location, $auth, $error) {

    this.isAuthenticated = function () {
        return $auth.isAuthenticated();
    };

    this.signOut = function() {
        $auth.signOut(
            function success() {
                $location.path('/sign-in/');

            },
            function error() {
                $location.path('/sign-in/');
            }
        );
    }
}