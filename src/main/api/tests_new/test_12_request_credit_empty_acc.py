import pytest
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты запроса кредита на пустой кредитный счёт"""


@pytest.mark.api
class TestRequestCredit:
    """Тест запроса кредита с валидными данными"""

    def test_request_credit(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        acc_id = response_create_credit_account.id
        credit_amount = 9999
        term_months = 33

        # тело запроса на получение кредита
        payload_request_credit = RequestCreditRequestModel(
            accountId=acc_id, amount=credit_amount, termMonths=term_months
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
        assert response_request_credit.balance == credit_amount

    """Тест запроса кредита с невалидными данными (запрос второго кредита на один счёт)"""

    def test_request_credit_invalid(self, create_credit_user, request_spec_credit_user):
        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        # тело запроса на запрос кредита
        # Минимальная сумма кредита - 5000, максимальная 15000
        # период кредита от 1 до 60 месяцев
        acc_id = response_create_credit_account.id
        credit_amount = 7777
        term_months = 22

        # тело запроса на получение кредита
        payload_request_credit = RequestCreditRequestModel(
            accountId=acc_id, amount=credit_amount, termMonths=term_months
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
