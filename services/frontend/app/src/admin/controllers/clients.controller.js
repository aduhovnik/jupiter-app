module = angular.module("jupiter.admin");
module.controller('ClientsController', ClientsController);


function ClientsController($http, $error, $auth) {
    var ctrl = this;

    this.getClients = function () {
        ctrl.data = [];
        $http.get($auth.addUrlAuth('/api/users/')).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };
}
