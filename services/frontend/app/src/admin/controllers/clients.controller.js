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

    this.activateClient = function(userId) {
        console.log(userId);
        $http.get($auth.addUrlAuth('/api/users/' + userId + '/activate/')).then(
            function success(response) {
                ctrl.getClients();
                ctrl.errors = response.data;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        )
    };

    this.deactivateClient = function(userId) {
        console.log(userId);
        $http.get($auth.addUrlAuth('/api/users/' + userId + '/deactivate/')).then(
            function success(response) {
                ctrl.getClients();
                ctrl.errors = response.data;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        )
    };
}
