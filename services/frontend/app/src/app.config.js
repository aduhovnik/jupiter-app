urls = {
    "/": "src/core/views/main.view.html",
    "/error/": "src/core/views/error.view.html",

    "/sign-in/": "src/auth/views/sign-in.view.html",
    '/sign-up/': "src/auth/views/sign-up.view.html",

    '/credits/templates/:id/': 'src/public/views/credit-template-detail.view.html',
    '/credits/templates/': 'src/public/views/credit-template-list.view.html',
    '/deposits/templates/:id/': 'src/public/views/deposit-template-detail.view.html',
    '/deposits/templates/': 'src/public/views/deposit-template-list.view.html',

    '/clients/': 'src/admin/views/clients-list.view.html'
};


var app = angular.module("jupiter", ["ngRoute", "jupiter.core", "jupiter.auth", "jupiter.public", "jupiter.admin"]);
app.config(function ($routeProvider, $locationProvider) {
    var routes = $routeProvider;
    for (var url in urls) {
        if (urls.hasOwnProperty(url)) {
            routes = routes.when(url, {templateUrl: urls[url]})
        }
    }
    $locationProvider.html5Mode({enabled: true, requireBase: true});
});
