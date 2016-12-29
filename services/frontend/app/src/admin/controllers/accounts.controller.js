module = angular.module("jupiter.admin");
module.controller("AccountsController", AccountsController);

function AccountsController($http, $auth, $error, $location, $url, accountStatuses) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.accountStatuses = accountStatuses;

    // TODO: extract common logic from controllers

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getAccounts = function () {
        ctrl.queryParams = {
            "number__startswith": ctrl.filterParams.number,
            "client__first_name__istartswith": ctrl.filterParams.name,
            "residue__gt": ctrl.filterParams.residue,
            "status__exact": ctrl.filterParams.status
        };

        var url = $auth.addUrlAuth('/api/accounts/');
        for (var key in ctrl.queryParams) {
            if (ctrl.queryParams.hasOwnProperty(key) && ctrl.queryParams[key]) {
                url = $url.query(url, key, ctrl.queryParams[key]);
            }
        }

        $http.get(url).then(
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

    ctrl.account_data = {
        account_number: ""
    };

    this.assignAccount = function () {
        var url = $auth.addUrlAuth('/api/accounts/assign/');
        $http.post(url, ctrl.account_data).then(
            function success(response) {
                ctrl.getAccounts();
                ctrl.errors = null;
                ctrl.success = 'Счет успешно добавлен'
            },
            function error(response) {
                ctrl.data = [];
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    };

    this.createRequest = function () {
        var url = $auth.addUrlAuth('/api/accounts/leave_create_claim/');
        $http.post(url, {}).then(
            function success(response) {
                ctrl.getAccounts();
                ctrl.errors = null;
                ctrl.success = response.data
            },
            function error(response) {
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    };

    this.confirmCreateRequest = function (id) {
        var url = $auth.addUrlAuth('/api/accounts/' + id + '/confirm_create_claim/');
        $http.post(url, {}).then(
            function success(response) {
                ctrl.getAccounts();
                ctrl.errors = null;
                ctrl.success = response.data
            },
            function error(response) {
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    };

    this.rejectCreateRequest = function (id) {
        var url = $auth.addUrlAuth('/api/accounts/' + id + '/reject_create_claim/');
        $http.post(url, {}).then(
            function success(response) {
                ctrl.getAccounts();
                ctrl.errors = null;
                ctrl.success = response.data
            },
            function error(response) {
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    };

    this.closeRequest = function(id) {
        var url = $auth.addUrlAuth('/api/accounts/' + id + '/leave_close_claim/');
        $http.post(url, {
            target_account_id: id
        }).then(
            function success(response) {
                ctrl.getAccounts();
                ctrl.errors = null;
                ctrl.success = response.data;
            },
            function error(response) {
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    }
}
