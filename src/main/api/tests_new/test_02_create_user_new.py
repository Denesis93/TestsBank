import pytest
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты создания юзера"""


@pytest.mark.api
class TestCreateUser:
    """Тест создания юзера с валидными данными"""

    def test_create_user_new(self, user_data, request_spec_admin, payload_create_user):

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_create_user)

        assert response_create_user.username == user_data["username"]
        assert response_create_user.role == user_data["role"]
        assert response_create_user.id > 0

    """Тест создания юзера с невалидными данными"""

    @pytest.mark.parametrize(
        "username, password",
        [
            ("Дэн", "Pas!sw0rd"),
            ("Denhkkhy89uljugyuggiuhgiu", "Pas!sw0rd"),
            ("Den!", "Pas!sw0rd"),
            ("Den", "пароль"),
        ],
    )
    def test_create_invalid_data(
        self, user_data, request_spec_admin, username, password
    ):

        # тело запроса на создание юзера с невалидными данными
        payload_create_user = CreateUserRequestModel(
            username=username, password=password, role="ROLE_USER"
        )

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload_create_user)

        assert "error" in response_create_user
