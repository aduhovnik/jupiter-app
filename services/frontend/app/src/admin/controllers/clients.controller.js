module = angular.module("jupiter.admin");
module.controller('ClientsController', ClientsController);


function ClientsController($http, $error, $auth, $routeParams, $scope, $filter, $location, $url) {
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

    ctrl.filterParams = $location.search();
    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    this.getClients = function () {
        ctrl.data = [];

        ctrl.queryParams = {
            "first_name__istartswith": ctrl.filterParams.name,
            "profile__identification_number__icontains": ctrl.filterParams.in,
            "profile__passport_number__istartswith": ctrl.filterParams.pn,
            "is_active": ctrl.filterParams.state
        };

        var url = $auth.addUrlAuth('/api/users/');
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
