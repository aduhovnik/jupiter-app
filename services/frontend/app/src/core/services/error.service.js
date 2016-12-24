module = angular.module("jupiter.core");
module.service("$error", ErrorService);

function ErrorService($location) {
    var self = this;
    this.onError = function (response) {
        if (response.status != 400) {
            self.globalHTTPError = {
                status: response.status,
                message: response.statusText
            };
            $location.path('/error/');

        }
    };

    this.onSuccess = function () {
        self.globalHTTPError = null;
    };

    this.getError = function () {
        return self.globalHTTPError;
    }

    this.hasError = function () {
        return self.globalHTTPError ? true : false;
    }
}
