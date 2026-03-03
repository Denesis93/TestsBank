import pytest
import random


@pytest.mark.api
def test_create_account(api_client, admin_token):
    """Создание юзера"""
    random_username = f"Denis{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для юзера"""
    user_token = response_user_auth.token

    """Создание банковского счёта"""
    account_create_response = api_client.create_account(user_token)

    assert account_create_response.id > 0
    assert account_create_response.number
    assert account_create_response.balance == 0


@pytest.mark.api
def test_create_more_2_accounts(api_client, admin_token):
    """Создание юзера"""
    random_username = f"Denis{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для юзера"""
    user_token = response_user_auth.token

    """Создание банковского счёта №1"""
    api_client.create_account(user_token)

    """Создание банковского счёта №2"""
    api_client.create_account(user_token)

    """Создание банковского счёта №3"""
    account_create_response = api_client.create_account_raw(user_token)
    assert account_create_response.status_code == 409
