module = angular.module("jupiter.admin", ["jupiter.auth", "ui.bootstrap"]);

module.constant(
    "creditStatuses",
    {
        0: "Открыт",
        1: "Штраф",
        2: "Выплачен",
        3: "Закрыт",
        4: "Отклонен",
        5: "Заявка"
    }
);

module.constant(
    "depositStatuses",
    {
        0: "Открыт",
        1: "Закрыт",
        2: "Отклонен",
        3: "Заявка"
    }
);

module.constant(
    "transactionTypes",
    {
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
    }
);