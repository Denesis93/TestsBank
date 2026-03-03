import pytest
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.login_user_requester import LoginUserPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""Тест на логин кредитного юзера"""


@pytest.mark.api
class TestCreditUserLogin:
    """Тест логина кредитного юзера с валидными данными"""

    def test_credit_user_login(self, create_credit_user, credit_user_data):

        # тело для запроса на логин кредитного пользователя
        payload_credit_user_login = LoginUserRequestModel(
            username=credit_user_data["username"], password=credit_user_data["password"]
        )

        # отправка запроса на логин кредитного пользователя
        response_credit_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_credit_user_login)

        assert response_credit_user_login.user.username == credit_user_data["username"]
        assert response_credit_user_login.user.role == credit_user_data["role"]
        assert response_credit_user_login.token

    """Тест логина кредитного юзера с неправильным паролем"""

    def test_invalid_login(
        self, credit_user_data, request_spec_admin, payload_create_credit_user
    ):

        # отправка запроса на создание юзера
        CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_create_credit_user)

        # тело запроса на логин юзера
        payload_user_login = LoginUserRequestModel(
            username=credit_user_data["username"], password="Pas!sw0rdO"
        )

        # отправка запроса на логин юзера
        response_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.unauthorized_status(),
        ).post(payload_user_login)

        assert response_user_login["error"] == "Invalid credentials"
