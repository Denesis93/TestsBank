import pytest
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs
import allure

"""Тесты на создание банковского счёта"""


@pytest.mark.api
class TestCreateAccount:
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
