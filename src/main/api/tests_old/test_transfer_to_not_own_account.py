import random
import pytest

"""Тест перевода денег на чужой счёт"""


@pytest.mark.api
def test_transfer_to_not_own_account(api_client, admin_token):
    """Создание юзера 1 (донор)"""
    random_username_1 = f"Darya{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username_1, role)
    username_1 = response_create_user.username

    """Аутентификация под юзером 1"""
    response_user_1_auth = api_client.user_login(username_1)

    """Получение токена авторизации для юзера 1"""
    user_1_token = response_user_1_auth.token

    """Создание юзера 2 (акцептор)"""
    random_username_2 = f"Darya{random.randint(1, 10000)}"
    response_create_user = api_client.create_user(admin_token, random_username_2, role)
    username_2 = response_create_user.username

    """Аутентификация под юзером 2"""
    response_user_2_auth = api_client.user_login(username_2)

    """Получение токена авторизации для юзера 2"""
    user_2_token = response_user_2_auth.token

    """Создание банковского счёта №1 (донор)"""
    account_create_response_1 = api_client.create_account(user_1_token)
    assert account_create_response_1.id > 0

    """Пополнение счёта №1"""
    amount_1 = random.randint(1000, 9000)
    acc_id_1 = account_create_response_1.id
    deposit_response_1 = api_client.deposit(user_1_token, acc_id_1, amount_1)
    assert deposit_response_1.balance == amount_1

    """Создание банковского счёта №2 (акцептор)"""
    account_create_response_2 = api_client.create_account(user_2_token)
    assert account_create_response_2.id > 0

    """Перевод средств на чужой счёт"""
    acc_id_2 = account_create_response_2.id
    amount_2 = round(random.uniform(500, deposit_response_1.balance), 2)
    transfer_response = api_client.transfer(acc_id_1, acc_id_2, user_1_token, amount_2)
    assert transfer_response.from_account_id == acc_id_1
    assert transfer_response.to_account_id == acc_id_2
    assert (
        transfer_response.from_account_id_balance
        == deposit_response_1.balance - amount_2
    )

    """Проверка, что переведённая сумма действительно появилась на втором счёте"""
    transactions = api_client.get_transactions_history(user_2_token, acc_id_2)
    assert transactions.id == acc_id_2
    assert transactions.transactions[0].amount == amount_2


@pytest.mark.parametrize(
    "amount, expected_status_code", [(499.99, 400), (10000.01, 400)]
)
@pytest.mark.api
def test_transfer_off_limits(api_client, admin_token, amount, expected_status_code):
    """Создание юзера 1 (донор)"""
    random_username_1 = f"Sergay{random.randint(1, 10000)}"
    role = "ROLE_USER"
    response_create_user = api_client.create_user(admin_token, random_username_1, role)
    username_1 = response_create_user.username

    """Аутентификация под юзером 1"""
    response_user_1_auth = api_client.user_login(username_1)

    """Получение токена авторизации для юзера 1"""
    user_1_token = response_user_1_auth.token

    """Создание юзера 2 (акцептор)"""
    random_username_2 = f"Darya{random.randint(1, 10000)}"
    response_create_user = api_client.create_user(admin_token, random_username_2, role)
    username_2 = response_create_user.username

    """Аутентификация под юзером 2"""
    response_user_2_auth = api_client.user_login(username_2)

    """Получение токена авторизации для юзера 2"""
    user_2_token = response_user_2_auth.token

    """Создание банковского счёта №1 (донор)"""
    account_create_response_1 = api_client.create_account(user_1_token)
    assert account_create_response_1.id > 0

    """Пополнение счёта №1"""
    amount_1 = random.randint(1000, 9000)
    acc_id_1 = account_create_response_1.id
    deposit_response_1 = api_client.deposit(user_1_token, acc_id_1, amount_1)
    assert deposit_response_1.balance == amount_1

    """Создание банковского счёта №2 (акцептор)"""
    account_create_response_2 = api_client.create_account(user_2_token)
    assert account_create_response_2.id > 0

    """Перевод средств вне допустимого минимума/максимума на чужой счёт """
    acc_id_2 = account_create_response_2.id
    transfer_response = api_client.transfer_raw(
        acc_id_1, acc_id_2, user_1_token, amount
    )
    assert transfer_response.status_code == expected_status_code
