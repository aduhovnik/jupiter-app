module = angular.module("jupiter.auth");
module.controller('SignInController', SignInController);

function SignInController($auth, $error) {
    this.credentials = {
        username: "",
        password: ""
    };

    this.signIn = function() {
        var ctrl = this;
        $auth.signIn(
            this.credentials,
            function success(response) {
            },
            function error(response) {
                console.log(response);
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };
}
