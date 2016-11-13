module = angular.module("jupiter.core");
module.service("$auth", AuthService);

function AuthService($http, $localStorage) {
    this.isAuthenticated = function() {
        var token = $localStorage.token;
        return token ? true: false;
    };

    this.signIn = function(credentials, onSuccess, onError) {
        $http.post('/api/sign-in/', credentials).then(
            function success(response) {
                $localStorage.token = response.data.token;
                onSuccess(response);
            },
            function error(response) {
               onError(response);
            }
        );
    };

    this.signOut = function(onSuccess, onError) {
        var token = $localStorage.token;
        if (token) {
            $http.get('api/sign-out/?token=' + token).then(
                function success(response) {
                    delete $localStorage.token;
                    onSuccess(response);
                },
                function error(response) {
                   onError(response);
                }
            )
        }
    }
}