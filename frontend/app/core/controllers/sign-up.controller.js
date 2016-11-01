module = angular.module("jupiter.core");
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
                $location.path('/');
            },
            function error(response) {
                ctrl.errors = response.data;
            }
        );
    };
}