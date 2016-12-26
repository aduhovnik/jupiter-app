module = angular.module("jupiter.admin");
module.controller("DepositsController", DepositsController);

function DepositsController($http, $auth, $error, $location, $url) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.depositStatuses = {
        0: "Открыт",
        1: "Закрыт",
        2: "Отклонен",
        3: "Заявка"
    };

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getTransactions = function () {
        ctrl.queryParams = {
            "client__first_name__icontains": ctrl.filterParams.client,
            "template__exact": ctrl.filterParams.template,
            "status__exact": ctrl.filterParams.status
        };

        var url = $auth.addUrlAuth('/api/deposits/');
        for (key in ctrl.queryParams) {
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

    this.getDepositTemplates = function () {
        ctrl.templates = [];
        $http.get('/api/deposits/templates/').then(
            function success(response) {
                ctrl.templates = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );
    };
}
