import pytest
import random

"""Тест создания юзера"""


@pytest.mark.api
def test_create_user(api_client, admin_token):
    """Создание пользователя"""
    random_username = f"Denis{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    assert response_create_user.id > 0
    assert response_create_user.username.startswith("Denis")
    assert response_create_user.role == "ROLE_USER"


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
@pytest.mark.api
def test_create_user_wrong(api_client, admin_token, username, password):
    response_create_user = api_client.create_user_raw(admin_token, username, password)
    assert response_create_user.status_code == 400
