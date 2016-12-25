module = angular.module("jupiter.auth");
module.service("$auth", AuthService);


function AuthService($http, $localStorage) {
    var service = this;

    this.signIn = function(credentials, onSuccess, onError) {
        $http.post('/api/sign-in/', credentials).then(
            function success(response) {
                $localStorage.token = response.data.token;
                $localStorage.user = response.data.user;
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
                    delete $localStorage.user;
                    if (onSuccess) {
                        onSuccess(response);
                    }
                },
                function error(response) {
                    delete $localStorage.token;
                    delete $localStorage.user;
                    if (onError) {
                       onError(response);
                    }
                }
            )
        }
    };

    this.signUp = function(userData, onSuccess, onError) {
        $http.post('api/sign-up/', userData).then(
            function success(response) {
                $localStorage.token = response.data.token;
                onSuccess(response);
            },
            function error(response) {
                onError(response)
            }
        )
    };

    this.addUrlAuth = function(url) {
        var token = $localStorage.token;
        return url + '?token=' + token;
    };
}
