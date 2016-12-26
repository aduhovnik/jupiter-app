module = angular.module("jupiter.admin");
module.controller('TransactionsController', TransactionsController);


function TransactionsController($http, $error, $auth, $location, $url, $scope, $filter) {
    var ctrl = this;
    ctrl.data = [];
    ctrl.filterParams = $location.search();
    ctrl.transactionTypes = {
        101: "Создание кредита",
        102: "Оплата по кредиту",
        103: "Закрытие кредита",
        104: "Начисление штрафа по кредиту",
        105: "Запрос на окрытие кредита",
        106: "Подтверждение открытия кредита",
        107: "Отклонение открытия кредита",
        108: "Открытие онлайн кредита",

        201: "Привязка счета",
        202: "Создание счета",
        203: "Запрос на создание счета",
        204: "Подтверждение создание счета",
        205: "Запрос на закрытие счета",
        206: "Подтверждение закрытия счета",
        207: "Отклонение открытия счета",
        208: "Отклонение закрытия счета",
        209: "Снятие средста со счета",
        210: "Зачисление средств на счет",

        301: "Добавление средств на вклад",
        302: "Создание вклада",
        303: "Заявка на открытие вклада",
        304: "Подтверждение открытия вклада",
        305: "Заявка на закрытие вклада",
        306: "Подтверждение закрытия вклада",
        307: "Отклонение открытия вклада",
        308: "Отклонение закрытия вклада",
        309: "Капитализация вклада",
        310: "Продление вклада",
        666: "Транзакция"
    };

    this.updateFilterParams = function(keyCode) {
        if (keyCode === 13) {
            $location.search(ctrl.filterParams);
        }
    };

    $scope.toogleStartDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.startDateOpened = !$scope.startDateOpened;
    };

    $scope.toogleEndDatePicker = function($event) {
        $event.preventDefault();
        $event.stopPropagation();
        $scope.endDateOpened = !$scope.endDateOpened;
    };

    this.getTransactions = function () {
        if (!ctrl.filterParams.startDate) {
            var previousMonth = new Date();
            previousMonth.setMonth(previousMonth.getMonth() - 1);
            ctrl.filterParams.startDate = previousMonth;
        }

        ctrl.queryParams = {
            "client__first_name__icontains": ctrl.filterParams.client,
            "product__name__istartswith": ctrl.filterParams.product,
            "type__exact": ctrl.filterParams.type,
            "created_on__gt": $filter('date')(ctrl.filterParams.startDate, 'yyyy-MM-dd 00:00'),
            "created_on__lt": $filter('date')(ctrl.filterParams.endDate, 'yyyy-MM-dd 00:00'),
            "ordering": "-created_on"
        };

        var url = $auth.addUrlAuth('/api/transactions/');
        for (key in ctrl.queryParams) {
            if (ctrl.queryParams.hasOwnProperty(key) && ctrl.queryParams[key]) {
                url = $url.query(url, key, ctrl.queryParams[key]);
            }
        }

        $http.get(url).then(
            function success(response) {
                ctrl.data = response.data;
                ctrl.errors = null;
            },
            function error(response) {
                ctrl.data = [];
                ctrl.errors = response.data;
                $error.onError(response);
            }
        );

        var startDate = ctrl.filterParams.startDate;
        ctrl.filterParams.startDate = $filter('date')(startDate, 'dd.MM.yyyy');

        var endDate = ctrl.filterParams.endDate;
        ctrl.filterParams.endDate = $filter('date')(endDate, 'dd.MM.yyyy');
    };
}
