import pytest
from main.api.models.deposit_request import DepositRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты пополнения кредитного счёта"""


@pytest.mark.api
class TestDepositCreditAcc:
    """Тест пополнения кредитного счёта валидными данными"""

    def test_deposit_credit_acc(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        account_id = response_create_account.id
        amount = 4444
        payload_deposit = DepositRequestModel(accountId=account_id, amount=amount)

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        assert response_deposit.balance == amount
        assert response_deposit.id == account_id

    """Тест пополнения счёта с невалидными данными (пополнение на сумму вне допустимого диапазона)"""

    @pytest.mark.parametrize("amount", [999.99, 9000.01])
    def test_deposit_invalid(
        self, create_credit_user, request_spec_credit_user, amount
    ):

        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        account_id = response_create_account.id
        payload_deposit = DepositRequestModel(accountId=account_id, amount=amount)

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload_deposit)

        assert response_deposit["error"] == "Amount must be between 1000 and 9000"
