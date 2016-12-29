module = angular.module("jupiter.auth");
module.controller('SignUpController', SignUpController);

function SignUpController($auth, $error) {

    this.data = {
        username: "",
        password: "",
        email: "",
        profile: {},
        first_name: "",
        last_name: ""
    };

    this.signUp = function() {
        var ctrl = this;
        $auth.signUp(
            this.data,
            function success() {
                ctrl.success = true;
            },
            function error(response) {
                ctrl.success = false;
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };
}