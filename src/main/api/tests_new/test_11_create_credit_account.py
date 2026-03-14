import pytest
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты на создание кредитного счёта"""


@pytest.mark.api
class TestCreateCreditAccount:

    """Тест создания кредитного банковского счёта с валидными данными"""

    def test_create_credit_account(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        assert response_create_credit_account.id > 0
        assert response_create_credit_account.balance == 0
        assert response_create_credit_account.number

    """Тест создания кредитного банковского счёта под админом (негативный сценарий)"""

    def test_create_credit_account_admin(self, request_spec_admin):

        # отправка запроса на создание банковского счёта
        response_create_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.forbidden_status(),
        ).post(None)

        assert response_create_account["error"] == "Admins cannot create bank accounts"
