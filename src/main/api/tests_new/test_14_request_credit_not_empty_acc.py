import pytest
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты запроса кредита на ранее пополненный счёт"""


@pytest.mark.api
class TestRequestDepositCreditAcc:
    """Тест запроса кредита с валидными данными"""

    def test_request_credit_acc(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        account_id = response_create_account.id
        amount = 5555
        payload_deposit = DepositRequestModel(accountId=account_id, amount=amount)

        # отправка запроса на пополнение счёта
        DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        credit_amount = 7777
        term_months = 33
        payload_request_credit = RequestCreditRequestModel(
            accountId=account_id, amount=credit_amount, termMonths=term_months
        )
        # отправка запроса на получение кредита
        response_request_credit = CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)

        assert response_request_credit.id > 0
        assert response_request_credit.credit_id > 0
        assert response_request_credit.amount == credit_amount
        assert response_request_credit.term_months == term_months
        assert response_request_credit.balance == credit_amount + amount

    """Тест запроса кредита с невалидными данными (запрос второго кредита на один счёт"""

    def test_request_credit_acc_invalid(
        self, create_credit_user, request_spec_credit_user
    ):
        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        account_id = response_create_account.id
        amount = 5555
        payload_deposit = DepositRequestModel(accountId=account_id, amount=amount)

        # отправка запроса на пополнение счёта
        DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        credit_amount = 7777
        term_months = 33
        payload_request_credit = RequestCreditRequestModel(
            accountId=account_id, amount=credit_amount, termMonths=term_months
        )
        # отправка запроса на получение первого кредита
        CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)

        # отправка запроса на получение второго кредита
        response_request_2nd_credit = CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.not_found_status(),
        ).post(payload_request_credit)

        # по сваггеру должна быть 403 ошибка, по факту 404
        assert (
            response_request_2nd_credit["error"]
            == "Only one active credit allowed per user"
        )
