module = angular.module("jupiter.public");
module.controller('DepositTemplatesController', DepositTemplatesController);


function DepositTemplatesController($http, $routeParams, $error, currencyNames) {
    var ctrl = this;
    ctrl.currencyNames = currencyNames;

    this.getDepositTemplates = function () {
        ctrl.data = [];
        $http.get('/api/deposits/templates/').then(
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

    this.getDepositTemplate = function () {
        ctrl.data = {};
        var url ='/api/deposits/templates/' + $routeParams["id"] + '/';
        $http.get(url).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.currency_data = Object.values(ctrl.data.currency);
                ctrl.errors = null;
            },
            $error.onError
        )
    }
}
