module = angular.module("jupiter.auth");
module.controller('SignInController', SignInController);

function SignInController($location, $auth, $error) {
    this.credentials = {
        username: "",
        password: ""
    };

    this.signIn = function() {
        var ctrl = this;
        ctrl.errors = [];
        $auth.signIn(
            this.credentials,
            function success(response) {
                $location.path('/');
            },
            function error(response) {
                console.log(response)
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };
}
