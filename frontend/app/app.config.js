urls = {
    "/": "core/views/home.view.html",
    "/sign-in": "/core/views/sign-in.view.html",
    '/sign-up': "/core/views/sign-up.view.html"
};


var app = angular.module("jupiter", ["ngRoute", "jupiter.core"]);
app.config(function ($routeProvider, $locationProvider) {
    var routes = $routeProvider;
    for (var url in urls) {
        if (urls.hasOwnProperty(url)) {
            routes = routes.when(url, {templateUrl: urls[url]})
        }
    }
    $locationProvider.html5Mode({enabled: true, requireBase: false});
});