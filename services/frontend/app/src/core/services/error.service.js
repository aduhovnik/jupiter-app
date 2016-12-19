module = angular.module("jupiter.core");
module.service("$error", ErrorService);

function ErrorService() {
    var self = this;
    this.onError = function (response) {
        if (response.status != 400) {
            self.globalHTTPError = {
                status: response.status,
                message: response.statusText
            };
        }
    };

    this.onSuccess = function () {
        self.globalHTTPError = null;
    };

    this.getError = function () {
        return self.globalHTTPError
    }
}