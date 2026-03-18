import pytest
from constants import AMOUNT_DEPOSIT
from main.api.models.deposit_request import DepositRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты для проверки работы с банковским счётом"""

@pytest.mark.api
class TestAccount:
    """Тест создания банковского счёта с валидными данными"""

    def test_create_account(
        self, user_data, request_spec_admin, create_user, request_spec_user
    ):
        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        assert response_create_account.id > 0
        assert response_create_account.balance == 0
        assert response_create_account.number

    """Тест создания банковского счёта под админом (негативный сценарий)"""

    def test_create_account_admin(self, request_spec_admin):
        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.forbidden_status(),
        ).post(None)

        assert response_create_account["error"] == "Admins cannot create bank accounts"

    """Тест пополнения счёта с валидными данными"""

    def test_deposit(
        self,
        user_data,
        request_spec_admin,
        create_user,
        request_spec_user,
        create_account,
    ):
        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000

        payload_deposit = DepositRequestModel(
            accountId=create_account.id, amount=AMOUNT_DEPOSIT
        )

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        assert response_deposit.balance == AMOUNT_DEPOSIT
        assert response_deposit.id == create_account.id

    """Тест пополнения счёта с невалидными данными (пополнение на сумму вне допустимого диапазона)"""

    @pytest.mark.parametrize("amount", [999.99, 9000.01])
    def test_deposit_invalid(
        self, create_user, request_spec_user, amount, create_account
    ):
        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        payload_deposit = DepositRequestModel(
            accountId=create_account.id, amount=amount
        )

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload_deposit)
