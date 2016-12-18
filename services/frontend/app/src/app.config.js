urls = {
    "/": "src/core/views/home.view.html",
    "/sign-in/": "src/auth/views/sign-in.view.html",
    '/sign-up/': "src/auth/views/sign-up.view.html",
    '/credits/templates/:id/': 'src/finance/views/credit-template-detail.view.html',
    '/credits/templates/': 'src/finance/views/credit-template-list.view.html',
    '/deposits/templates/:id/': 'src/finance/views/deposit-template-detail.view.html',
    '/deposits/templates/': 'src/finance/views/deposit-template-list.view.html'
};


var app = angular.module("jupiter", ["ngRoute", "jupiter.core", "jupiter.auth", "jupiter.finance"]);
app.config(function ($routeProvider, $locationProvider) {
    var routes = $routeProvider;
    for (var url in urls) {
        if (urls.hasOwnProperty(url)) {
            routes = routes.when(url, {templateUrl: urls[url]})
        }
    }
    $locationProvider.html5Mode({enabled: true, requireBase: true});
});