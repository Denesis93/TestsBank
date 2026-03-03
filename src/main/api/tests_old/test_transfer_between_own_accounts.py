import random
import pytest

"""Тест перевода денег между своими счетами"""


@pytest.mark.api
def test_transfer_between_own_accounts(api_client, admin_token):
    """Создание юзера"""
    random_username = f"Andrey{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для юзера"""
    user_token = response_user_auth.token

    """Создание банковского счёта №1 (донор)"""
    account_create_response_1 = api_client.create_account(user_token)
    assert account_create_response_1.id > 0

    """Пополнение счёта №1"""
    amount_1 = random.randint(1000, 9000)
    acc_id_1 = account_create_response_1.id
    deposit_response_1 = api_client.deposit(user_token, acc_id_1, amount_1)
    assert deposit_response_1.balance == amount_1

    """Создание счёта №2 (приёмник)"""
    account_create_response_2 = api_client.create_account(user_token)
    assert account_create_response_2.id > 0
    acc_id_2 = account_create_response_2.id

    """Перевод денежных средств"""
    amount_2 = round(random.uniform(500, deposit_response_1.balance), 2)
    transfer_response = api_client.transfer(acc_id_1, acc_id_2, user_token, amount_2)
    assert transfer_response.from_account_id == acc_id_1
    assert transfer_response.to_account_id == acc_id_2
    assert (
        transfer_response.from_account_id_balance
        == deposit_response_1.balance - amount_2
    )

    """Проверка, что переведённое количество действительно появилось на втором счёте"""
    transactions = api_client.get_transactions_history(user_token, acc_id_2)
    assert transactions.id == acc_id_2
    assert transactions.transactions[0].amount == amount_2


@pytest.mark.parametrize(
    "amount, expected_status_code", [(499.99, 400), (10000.01, 400)]
)
@pytest.mark.api
def test_transfer_off_limits(api_client, admin_token, amount, expected_status_code):
    """Создание юзера"""
    random_username = f"Oleg{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для юзера"""
    user_token = response_user_auth.token

    """Создание банковского счёта №1 (донор)"""
    account_create_response_1 = api_client.create_account(user_token)
    assert account_create_response_1.id > 0

    """Пополнение счёта №1"""
    amount_1 = random.randint(1000, 9000)
    acc_id_1 = account_create_response_1.id
    deposit_response_1 = api_client.deposit(user_token, acc_id_1, amount_1)
    assert deposit_response_1.balance == amount_1

    """Создание счёта №2 (приёмник)"""
    account_create_response_2 = api_client.create_account(user_token)
    acc_id_2 = account_create_response_2.id

    """Перевод денежных средств вне допустимых значений"""
    transfer_response = api_client.transfer_raw(acc_id_1, acc_id_2, user_token, amount)
    assert transfer_response.status_code == expected_status_code
