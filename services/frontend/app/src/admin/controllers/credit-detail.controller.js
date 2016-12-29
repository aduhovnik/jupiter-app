module = angular.module('jupiter.admin');
module.controller('CreditDetailController', CreditDetailController);


function CreditDetailController(
    $http, $auth, $routeParams, creditStatuses, accountStatuses, $route, $scope
) {
    var ctrl = this;

    ctrl.credit = null;
    ctrl.errors = null;
    ctrl.accounts = null;
    ctrl.creditStatuses = creditStatuses;
    ctrl.accountStatuses = accountStatuses;

    ctrl.getData = function() {
        var url ="/api/credits/" + $routeParams["id"] + "/";
        $http.get($auth.addUrlAuth(url)).then(function success(response) {
            ctrl.credit = response.data;
            ctrl.errors = null;
        }, function error(response) {
            ctrl.errors = response.data;
        });
        url = "/api/accounts/";
        $http.get($auth.addUrlAuth(url)).then(function success(response) {
            ctrl.accounts = response.data;
        }, function error(response) {
            // TODO: join errors
            ctrl.errors = response.data;
        });
    };

    ctrl.canClose = function() {
        return $scope.user.isClient() &&
                ctrl.credit.status === 0;
    };

    ctrl.close = function() {
        var url = "/api/credits/" + $routeParams["id"] + "/close/";
        $http.patch($auth.addUrlAuth(url), {}).then(function success(response) {
            $route.reload();
        }, function error(response) {
            ctrl.errors = response.data;
        });
    };

    ctrl.pay = function(amount, account_id) {
        var url = "/api/credits/" + $routeParams["id"] + "/make_payment/";
        $http.post($auth.addUrlAuth(url), {
            amount: amount,
            account_id: account_id
        }).then(function success() {
            $route.reload();
        }, function error(response) {
            ctrl.errors = response.data;
        });
    }
}