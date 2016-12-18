module = angular.module("jupiter.core");
module.controller('ErrorController', ErrorController);

function ErrorController($routeParams) {
    this.error = {
        "status": $routeParams.status,
        "message": $routeParams.message
    }
}
