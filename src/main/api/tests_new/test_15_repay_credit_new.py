import pytest
from main.api.models.repay_credit_request import RepayCreditRequestModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.repay_credit_requester import RepayCreditPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты погашения кредита"""


@pytest.mark.api
class TestRequestCredit:
    """Тест погашения кредита с валидными данными"""

    def test_repay_credit(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        acc_id = response_create_credit_account.id
        credit_amount = 6666
        term_months = 22

        # тело запроса на запрос кредита
        payload_request_credit = RequestCreditRequestModel(
            accountId=acc_id, amount=credit_amount, termMonths=term_months
        )

        # отправка запроса на запрос кредита
        response_request_credit = CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)

        # тело запроса на погашение кредита
        credit_id = response_request_credit.credit_id
        repay_amount = response_request_credit.amount
        payload_repay_credit = RepayCreditRequestModel(
            creditId=credit_id, accountId=acc_id, amount=credit_amount
        )
        response_repay_credit = RepayCreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_repay_credit)

        assert response_repay_credit.creditId == credit_id
        assert response_repay_credit.amount_deposited == repay_amount

    """Тест погашения кредита с невалидными данными (погашение на недостаточную сумму)"""

    def test_repay_credit_invalid(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        acc_id = response_create_credit_account.id
        credit_amount = 5555
        term_months = 12

        # тело запроса на запрос кредита
        payload_request_credit = RequestCreditRequestModel(
            accountId=acc_id, amount=credit_amount, termMonths=term_months
        )

        # отправка запроса на запрос кредита
        response_request_credit = CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)

        # тело запроса на погашение кредита
        credit_id = response_request_credit.credit_id
        # repay_amount = response_request_credit.amount

        # тело запроса на погашение кредита
        payload_repay_credit = RepayCreditRequestModel(
            creditId=credit_id, accountId=acc_id, amount=5554.99
        )

        # отправка запроса на погашение кредита с недостаточной суммой для погашения
        response_repay_credit = RepayCreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.unprocessable_status(),
        ).post(payload_repay_credit)

        assert (
            response_repay_credit["error"]
            == f"The amount is not enough. Credit balance: -{response_request_credit.balance:.0f}"
        )
