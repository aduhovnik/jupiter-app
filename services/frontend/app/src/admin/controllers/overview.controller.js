module = angular.module("jupiter.admin");
module.controller('OverviewController', OverviewController);


function OverviewController($http, $error, $auth,
                           creditStatuses, depositStatuses, accountStatuses) {
    var ctrl = this;
    ctrl.creditStatuses = creditStatuses;
    ctrl.depositStatuses = depositStatuses;
    ctrl.accountStatuses = accountStatuses;
    ctrl.userStatuses = {
        "True": "Активен",
        "False": "Деактивирован"
    };

    ctrl.statistics = {};
    this.getInfo = function () {
        var url = $auth.addUrlAuth('/api/users/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.users = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
        
        url = $auth.addUrlAuth('/api/accounts/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.accounts = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );

        url = $auth.addUrlAuth('/api/deposits/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.deposits = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );

        url = $auth.addUrlAuth('/api/credits/info/');
        $http.get(url).then(
            function success(response) {
                ctrl.statistics.credits = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    }
}