import pytest
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты создания кредитного юзера"""


@pytest.mark.api
class TestCreateCreditUser:
    """Тест создания кредитного юзера с валидными данными"""

    def test_create_credit_user(
        self, credit_user_data, request_spec_admin, payload_create_credit_user
    ):

        # отправка запроса на создание кредитного юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).post(payload_create_credit_user)

        assert response_create_user.role == credit_user_data["role"]
        assert response_create_user.id > 0
        assert response_create_user.username == credit_user_data["username"]

    """Тест создания кредитного юзера с невалидными данными"""

    @pytest.mark.parametrize(
        "username, password",
        [
            ("Дэн", "Pas!sw0rd"),
            ("Denhkkhy89uljugyuggiuhgiu", "Pas!sw0rd"),
            ("Den!", "Pas!sw0rd"),
            ("Den", "пароль"),
        ],
    )
    def test_create_credit_user_invalid(
        self, credit_user_data, request_spec_admin, username, password
    ):

        # тело запроса, передающееся через модель
        payload = CreateUserRequestModel(
            username=username,
            password=password,
            role=credit_user_data["role"],
        )

        # отправка запроса на создание кредитного юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload)

        assert "error" in response_create_user
