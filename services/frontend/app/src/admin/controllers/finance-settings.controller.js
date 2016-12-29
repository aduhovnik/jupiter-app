module = angular.module("jupiter.admin");
module.controller("FinanceSettingsController", FinanceSettingsController);


function FinanceSettingsController($http, $auth, $error) {
    var ctrl = this;
    ctrl.data = [];

    this.getFinanceSettings = function () {
        var url = $auth.addUrlAuth('api/settings/meow/');
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

    this.updateScoringValues = function () {
        var url = $auth.addUrlAuth('api/settings/meow/');
        $http.patch(url, ctrl.data).then(
            function success(response) {
                ctrl.getFinanceSettings();
                ctrl.errors = null;
                ctrl.success = 'Критические уровни скоринга успешно изменены'
            },
            function error(response) {
                ctrl.errors = response.data;
                ctrl.success = null;
                $error.onError(response);
            }
        );
    };
}
