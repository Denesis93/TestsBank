import pytest
from constants import AMOUNT_DEPOSIT
from main.api.models.deposit_request import DepositRequestModel
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты пополнения кредитного счёта"""

@pytest.mark.api
class TestDepositCreditAcc:

    """Тест пополнения кредитного счёта валидными данными"""

    def test_deposit_credit_acc(self, create_credit_user, request_spec_credit_user, create_credit_account):

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        payload_deposit = DepositRequestModel(accountId=create_credit_account.id, amount=AMOUNT_DEPOSIT)

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        assert response_deposit.balance == AMOUNT_DEPOSIT
        assert response_deposit.id == create_credit_account.id

    """Тест пополнения счёта с невалидными данными (пополнение на сумму вне допустимого диапазона)"""

    @pytest.mark.parametrize("amount_deposit_invalid", [999.99, 9000.01])
    def test_deposit_invalid(
        self, create_credit_user, request_spec_credit_user, amount_deposit_invalid, create_credit_account
    ):

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        payload_deposit = DepositRequestModel(accountId=create_credit_account.id, amount=amount_deposit_invalid)

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload_deposit)

        assert response_deposit["error"] == "Amount must be between 1000 and 9000"
