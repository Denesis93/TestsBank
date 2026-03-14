import pytest
from constants import AMOUNT_DEPOSIT
from main.api.models.deposit_request import DepositRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты пополнения счёта"""


@pytest.mark.api
class TestDeposit:
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

        assert response_deposit["error"] == "Amount must be between 1000 and 9000"
