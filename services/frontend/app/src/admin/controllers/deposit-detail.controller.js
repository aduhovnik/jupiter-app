module = angular.module('jupiter.admin');
module.controller('DepositDetailController', DepositDetailController);


function DepositDetailController(
    $http, $auth, $routeParams, depositStatuses, accountStatuses, $route, $scope
) {
    var ctrl = this;

    ctrl.deposit = null;
    ctrl.errors = null;
    ctrl.accoiunts = null;
    ctrl.depositStatuses = depositStatuses;
    ctrl.accountStatuses = accountStatuses;
    ctrl.account_id = null;

    ctrl.getData = function() {
        var url ="/api/deposits/" + $routeParams["id"] + "/";
        $http.get($auth.addUrlAuth(url)).then(function success(response) {
            ctrl.deposit = response.data;
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

    ctrl.close = function(account_id) {
        var url = "/api/deposits/" + $routeParams["id"] + "/leave_close_claim/";
        $http.patch($auth.addUrlAuth(url), {
            target_account_id: account_id
        }).then(function success(response) {
            $route.reload();
        }, function error(response) {
            ctrl.errors = response.data;
        });
    };
}