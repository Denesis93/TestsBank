import pytest
from main.api.models.admin_login_request import AdminLoginRequestModel
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.login_user_requester import LoginUserPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""Тесты логина"""


@pytest.mark.api
class TestLogin:
    """Тест логина под админом"""

    def test_admin_login(self):
        payload_login_admin = AdminLoginRequestModel(
            username="admin", password="123456"
        )

        response = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_login_admin)
        assert response.user.username == payload_login_admin.username
        assert response.user.role == "ROLE_ADMIN"

    """Тест логина под юзером с валидными данными"""

    def test_user_login(self, user_data, create_user):

        # тело запроса на логин юзера
        payload_user_login = LoginUserRequestModel(
            username=user_data["username"], password=user_data["password"]
        )

        # отправка запроса на логин юзера
        response_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_user_login)

        assert response_user_login.user.username == user_data["username"]
        assert response_user_login.user.role == user_data["role"]
        assert response_user_login.token

    """Тест логина юзера с неправильным паролем"""

    def test_invalid_login(self, user_data, create_user):

        # тело запроса на логин юзера
        payload_user_login = LoginUserRequestModel(
            username=user_data["username"], password="Pas!sw0rdD"
        )

        # отправка запроса на логин юзера
        response_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.unauthorized_status(),
        ).post(payload_user_login)

        assert response_user_login["error"] == "Invalid credentials"
