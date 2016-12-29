module = angular.module("jupiter.admin");
module.controller('SidebarController', SidebarController);


function SidebarController($location, $scope) {
    var ctrl = this;
    ctrl.items = [];

    this.valueIfPath = function(path, value) {
        return ($location.path().substr(0, path.length) === path) ? value : '';
    };

    this.initItems = function() {
        if ($scope.user.isAdmin()) {
            ctrl._addItem('/overview/', 'Сводка');
            ctrl._addItem('/clients/', 'Клиенты');
            ctrl._addItem('/accounts/', 'Cчета');
            ctrl._addItem('/credits/', 'Кредиты');
            ctrl._addItem('/deposits/', 'Вклады');
            ctrl._addItem('/transactions/', 'Транзакции');
            ctrl._addItem('/credit-templates/', 'Планы кредитов');
            ctrl._addItem('/deposit-templates/', 'Планы депозитов');
        }
        if ($scope.user.isClient()) {
            // ctrl._addItem('/overview/', 'Сводка');
            ctrl._addItem('/clients/me/', "Мой профайл");
            ctrl._addItem('/accounts/', 'Мои счета');
            ctrl._addItem('/credits/', 'Мои кредиты');
            ctrl._addItem('/credit-templates/', 'Оформление кредитов');
            ctrl._addItem('/deposits/', 'Мои вклады');
            ctrl._addItem('/deposit-templates/', 'Оформление вкладов');
            ctrl._addItem('/transactions/', 'Мои транзакции');
        }
    };

    this._addItem = function(url, label) {
        ctrl.items.push({
            url: url,
            label: label
        });
    };
}
