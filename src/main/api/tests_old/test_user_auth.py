import pytest
import random

"""Тест аутентификации под юзером"""


@pytest.mark.api
def test_auth_user(api_client, admin_token):
    """Создание юзера"""
    random_username = f"Denis{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентифицируемся под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получаем токен авторизации для юзера"""
    user_token = response_user_auth.token
    assert user_token
    assert response_user_auth.user.username == username
    assert response_user_auth.user.role == "ROLE_USER"
