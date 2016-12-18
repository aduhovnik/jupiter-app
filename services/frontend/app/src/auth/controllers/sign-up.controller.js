module = angular.module("jupiter.auth");
module.controller('SignUpController', SignUpController);

function SignUpController($http, $location) {
    this.data = {
        username: "",
        password: "",
        email: "",
        first_name: "",
        last_name: ""
    };

    this.signUp = function() {
        var ctrl = this;
        $http.post('/api/sign-up/', this.data).then(
            function success() {
                ctrl.success = true;
            },
            function error(response) {
                ctrl.errors = response.data;
            }
        );
    };
}