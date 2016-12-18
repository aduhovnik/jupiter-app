module = angular.module("jupiter.finance");
module.controller('CreditTemplatesController', CreditTemplatesController);


function CreditTemplatesController($http, $routeParams, $error) {
    var ctrl = this;

    this.getCreditTemplates = function () {
        ctrl.data = [];
        $http.get('/api/credits/templates/').then(
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

    this.getCreditTemplate = function () {
        ctrl.data = {};
        var url ='/api/credits/templates/' + $routeParams["id"] + '/';
        $http.get(url).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.errors = null;
            },
            $error.onError
        )
    }
}