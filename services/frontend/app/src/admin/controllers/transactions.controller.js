module = angular.module("jupiter.admin");
module.controller('TransactionsController', TransactionsController);


function TransactionsController($http, $error, $auth) {
    var ctrl = this;
    ctrl.data = [];

    this.getData = function () {
        $http.get($auth.addUrlAuth('/api/transactions/')).then(
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
