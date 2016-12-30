module = angular.module("jupiter.auth");
module.controller('PasswordResetController', PasswordResetController);


function PasswordResetController($auth, $error, $location) {
    this.reset_data = {
        email: ""
    };

    this.confirm_data = {
        key: "",
        new_password: "",
        new_password_confirm: ""
    };

    this.passwordReset = function() {
        var ctrl = this;
        $auth.passwordReset(
            this.reset_data,
            function success(response) {
                $location.path('/password-reset-confirm/');
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

    this.passwordResetConfirm = function() {
        var ctrl = this;
        $auth.passwordResetConfirm(
            this.confirm_data,
            function success(response) {
                $location.path('/sign-in/');
                $error.clearErrors();
            },
            function error(response) {
                $error.onError(response);
            }
        );
    };

}
