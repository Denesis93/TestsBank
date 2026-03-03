import pytest
import random

"""Тест создания кредитного счёта"""


@pytest.mark.api
def test_create_credit_account(api_client, admin_token):
    """Создание кредит-юзера"""
    username = f"Alex{random.randint(1, 10000)}"
    role = "ROLE_CREDIT_SECRET"
    response_create_user = api_client.create_user(admin_token, username, role)
    username = response_create_user.username

    """Аутентификация под кредит-юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для кредит-юзера"""
    user_token = response_user_auth.token

    """Создание кредитного счёта"""
    account_create_response = api_client.create_account(user_token)

    assert account_create_response.id > 0
    assert account_create_response.number
    assert account_create_response.balance == 0
