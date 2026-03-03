import random
import pytest

"""Тест запроса кредита"""


@pytest.mark.api
def test_request_credit(api_client, admin_token):
    """Создание кредит-юзера"""
    random_username = f"Alex{random.randint(1, 10000)}"
    role = "ROLE_CREDIT_SECRET"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под кредит-юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для кредит-юзера"""
    credit_user_token = response_user_auth.token

    """Создание кредитного счёта"""
    create_credit_account_response = api_client.create_account(credit_user_token)
    credit_acc_balance = create_credit_account_response.balance

    """Запрос кредита"""
    credit_acc_id = create_credit_account_response.id
    credit_amount = 5000
    term_months = 15

    request_credit_response = api_client.request_credit(
        credit_user_token, credit_acc_id, credit_amount, term_months
    )

    # assert request_credit_response.creditId > 0 #на самом деле здесь приходит id, а не accountId. В сваггере ошибка
    assert request_credit_response.id > 0
    assert request_credit_response.credit_id > 0
    assert request_credit_response.id == credit_acc_id
    assert request_credit_response.amount == credit_amount
    assert request_credit_response.term_months == term_months
    assert request_credit_response.balance == credit_acc_balance + credit_amount


@pytest.mark.api
def test_request_another_credit(api_client, admin_token):
    """Создание кредит-юзера"""
    random_username = f"Ilya{random.randint(1, 10000)}"
    role = "ROLE_CREDIT_SECRET"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под кредит-юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для кредит-юзера"""
    credit_user_token = response_user_auth.token

    """Создание кредитного счёта №1"""
    create_credit_account_response_1 = api_client.create_account(credit_user_token)

    """Создание кредитного счёта №2"""
    create_credit_account_response_2 = api_client.create_account(credit_user_token)
    assert create_credit_account_response_2.id > 0

    """Запрос кредита на 1й счёт"""
    credit_acc_id_1 = create_credit_account_response_1.id
    credit_amount = 13000
    term_months = 1

    api_client.request_credit(
        credit_user_token, credit_acc_id_1, credit_amount, term_months
    )

    """Запрос кредита на 2й счёт"""
    credit_acc_id_2 = create_credit_account_response_2.id
    credit_amount = 11000
    term_months = 5

    request_credit_response = api_client.request_credit_raw(
        credit_user_token, credit_acc_id_2, credit_amount, term_months
    )
    assert (
        request_credit_response.status_code == 404
    ), f"Status: {request_credit_response.status_code}, body: {request_credit_response.text}"  # снова ошибка: по сваггеру должна возвращаться 403 ошибка, а по факту 404


@pytest.mark.parametrize(
    "amount, term_months, expected_status_code",
    [(4999.99, 5, 400), (15000.01, 5, 400), (8000, 0, 400), (9000, 61, 400)],
)
@pytest.mark.api
def test_request_credit_off_limits(
    api_client, admin_token, amount, term_months, expected_status_code
):
    """Создание кредит-юзера"""
    random_username = f"Vadim{random.randint(1, 10000)}"
    role = "ROLE_CREDIT_SECRET"
    response_create_user = api_client.create_user(admin_token, random_username, role)
    username = response_create_user.username

    """Аутентификация под кредит-юзером"""
    response_user_auth = api_client.user_login(username)

    """Получение токена авторизации для кредит-юзера"""
    credit_user_token = response_user_auth.token

    """Создание кредитного счёта"""
    create_credit_account_response = api_client.create_account(credit_user_token)

    """Запрос кредита"""
    credit_acc_id = create_credit_account_response.id

    request_credit_response = api_client.request_credit_raw(
        credit_user_token, credit_acc_id, amount, term_months
    )
    assert request_credit_response.status_code == expected_status_code
