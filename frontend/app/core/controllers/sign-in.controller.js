module = angular.module("jupiter.core");
module.controller('SignInController', SignInController);

function SignInController($location, $auth) {
    this.credentials = {
        username: "",
        password: ""
    };

    this.signIn = function() {
        var ctrl = this;
        $auth.signIn(
            this.credentials,
            function success(response) {
                $location.path('/');
            },
            function error(response) {
                ctrl.errors = response.data;
            }
        );
    };
}