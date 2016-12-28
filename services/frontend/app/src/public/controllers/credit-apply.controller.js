module = angular.module("jupiter.public");
module.controller("CreditApplicationController", CreditApplicationController);


function CreditApplicationController(
    $http, $routeParams, ensuringMethods, moneyDestinations, $error, $auth, $location
) {
    var ctrl = this;
    ctrl.ensuringMethods = ensuringMethods;
    ctrl.moneyDestinations = moneyDestinations;

    ctrl.template = null;
    ctrl.account_id = null;
    ctrl.accounts = null;
    ctrl.duration = null;
    ctrl.amount = null;
    ctrl.ensuringMethod = null;
    ctrl.moneyDestination = "0"; // into account by default

    this.getData = function () {
        var url ='/api/credits/templates/' + $routeParams["id"] + '/';
        $http.get($auth.addUrlAuth(url)).then(
            function success(response) {
                ctrl.template = response.data;
                ctrl.errors = null;
            },
            $error.onError
        );
        $http.get($auth.addUrlAuth("/api/accounts/")).then(
            function success(response) {
                ctrl.accounts = response.data;
                ctrl.errors = null;
            },
            $error.onError
        );
    };

    this.apply = function() {
        if (!ctrl.template) {
            return;
        }
        var method = ctrl.template.issue_online ? 'open_online' : 'leave_create_claim';
        var url = '/api/credits/' + method + '/';
        $http.post($auth.addUrlAuth(url), {
            account_id: ctrl.account_id,
            template_id: ctrl.template.id,
            duration: ctrl.duration,
            amount: ctrl.amount,
            ensuring_method: ctrl.ensuringMethod,
            money_destination: ctrl.moneyDestination
        }).then(function success() {
            $location.path("/credits/");
        }, function error(response) {
            ctrl.errors = response.data;
        });
    };
}
