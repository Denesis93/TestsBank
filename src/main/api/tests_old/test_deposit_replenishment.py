import pytest
import random

"""Тест пополнения счёта"""


@pytest.mark.api
def test_deposit(api_client, admin_token):
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

    """Пополняем счёт 1й раз"""
    amount_1 = random.randint(1000, 9000)
    acc_id = account_create_response.id
    deposit_response = api_client.deposit(user_token, acc_id, amount_1)
    assert deposit_response.balance == amount_1
    assert deposit_response.id > 0

    """Повторное пополнение счёта"""
    amount_2 = random.randint(1000, 9000)
    deposit_response = api_client.deposit(user_token, acc_id, amount_2)
    assert deposit_response.balance == amount_1 + amount_2

    """Тест перевода средств вне минимального/максимального значения"""


@pytest.mark.parametrize(
    "amount, expected_status_code",
    [
        (999.99, 400),
        (9000.01, 400),
    ],
)
@pytest.mark.api
def test_off_limit_deposit(api_client, admin_token, amount, expected_status_code):
    """Создание юзера"""
    random_username = f"Olga{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для юзера"""
    user_token = response_user_auth.token

    """Создание банковского счёта"""
    account_create_response = api_client.create_account(user_token)

    """Пополнение счёта вне допустимых значений"""
    acc_id = account_create_response.id
    deposit_response = api_client.deposit_raw(user_token, acc_id, amount)
    assert deposit_response.status_code == expected_status_code
