module = angular.module("jupiter.admin");
module.controller("DepositsController", DepositsController);

function DepositsController($http, $auth, $error) {
    var ctrl = this;
    ctrl.data = [];

    // TODO: extract common logic from controllers

    this.getData = function () {
        $http.get($auth.addUrlAuth('/api/deposits/')).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.data = [];
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };

    ctrl.getData();
}
