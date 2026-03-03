import random
import pytest
import names

from main.api.models.create_user_request import CreateUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""""Фиктсуры для обычного пользователя""" ""

"""Данные для обычного пользователя"""


@pytest.fixture
def user_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 1000)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_USER",
    }


"""Данные для обычного 2го пользователя (для тестов, где нужно создавать 2х разных юзеров)"""


@pytest.fixture
def user_2_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 1000)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_USER",
    }


"""Реквест-спек для админа"""


@pytest.fixture
def request_spec_admin():
    return RequestSpecs.login_and_get_request_spec("admin", "123456")


"""Тело для запроса на создание обычного юзера"""


@pytest.fixture
def payload_create_user(user_data):
    return CreateUserRequestModel(
        username=user_data["username"],
        password=user_data["password"],
        role=user_data["role"],
    )


"""Тело для запроса на создание обычного юзера 2"""


@pytest.fixture
def payload_create_user_2(user_2_data):
    return CreateUserRequestModel(
        username=user_2_data["username"],
        password=user_2_data["password"],
        role=user_2_data["role"],
    )


"""Фикстура, создающая обычного пользователя"""


@pytest.fixture
def create_user(user_data, payload_create_user, request_spec_admin):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_user)


"""Фикстура, создающая пользователя 2"""


@pytest.fixture
def create_user_2(user_2_data, payload_create_user_2, request_spec_admin):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_user_2)


"""Реквест-спек для обычного юзера"""


@pytest.fixture
def request_spec_user(user_data):
    username = user_data["username"]
    password = user_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)


"""Реквест-спек для юзера 2"""


@pytest.fixture
def request_spec_user_2(user_2_data):
    username = user_2_data["username"]
    password = user_2_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)


"""""Фиктсуры для кредитного пользователя""" ""

"""Данные для кредитного пользователя"""


@pytest.fixture
def credit_user_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 100)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_CREDIT_SECRET",
    }


"""Тело для запроса на создание кредитного юзера"""


@pytest.fixture
def payload_create_credit_user(credit_user_data):
    return CreateUserRequestModel(
        username=credit_user_data["username"],
        password=credit_user_data["password"],
        role=credit_user_data["role"],
    )


"""Фикстура, создающая кредитного пользователя"""


@pytest.fixture
def create_credit_user(
    credit_user_data, payload_create_credit_user, request_spec_admin
):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_credit_user)


"""Реквест-спек для кредитного юзера"""


@pytest.fixture
def request_spec_credit_user(credit_user_data):
    username = credit_user_data["username"]
    password = credit_user_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)
