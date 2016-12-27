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
            "residue__amount__equals": ctrl.filterParams.residue,
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
}
