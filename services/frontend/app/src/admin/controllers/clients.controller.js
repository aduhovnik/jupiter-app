module = angular.module("jupiter.admin");
module.controller('ClientsController', ClientsController);


function ClientsController($http, $error, $auth, $routeParams, $scope, $filter) {
    var ctrl = this;

    $scope.toogleBirthDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.birthDatePickerOpened = !$scope.birthDatePickerOpened;
    };

    $scope.tooglePassportExpiresPicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.passportExpiresPickerOpened = !$scope.passportExpiresPickerOpened;
    };

    this.getClients = function () {
        ctrl.data = [];
        $http.get($auth.addUrlAuth('/api/users/')).then(
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

    this.getClient = function () {
        ctrl.data = [];
        $http.get($auth.addUrlAuth('/api/users/' + $routeParams['id'] + '/')).then(
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

    this.activateClient = function(userId) {
        $http.get($auth.addUrlAuth('/api/users/' + userId + '/activate/')).then(
            function success(response) {
                ctrl.getClients();
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        )
    };

    this.deactivateClient = function(userId) {
        $http.get($auth.addUrlAuth('/api/users/' + userId + '/deactivate/')).then(
            function success(response) {
                ctrl.getClients();
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        )
    };

    this.updateClient = function(userId) {
        var birthDate = ctrl.data.profile.birth_date;
        ctrl.data.profile.birth_date = $filter('date')(birthDate, 'yyyy-MM-dd');

        var passportExpires = ctrl.data.profile.passport_expires;
        ctrl.data.profile.passport_expires = $filter('date')(passportExpires, 'yyyy-MM-dd');

        $http.patch($auth.addUrlAuth('/api/users/' + userId + '/'), ctrl.data).then(
            function success(response) {
                ctrl.getClient();
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.errors = response.data;
                $error.onError(response);
            }
        )
    }
}
