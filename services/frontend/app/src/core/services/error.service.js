module = angular.module("jupiter.core");
module.service("$error", ErrorService);

function ErrorService($rootScope) {
    this.onError = function (response) {
        if (!(response.status in [400])) {
            $rootScope.globalHTTPError = {
                status: response.status,
                message: response.statusText
            };
        }
    }
}