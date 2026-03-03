import random
import pytest

"""Тест погашения кредита"""


@pytest.mark.api
def test_repay_credit(api_client, admin_token):
    # """Создание кредит-юзера"""
    # random_username = f"Lisa{random.randint(1, 10000)}"
    # role = "ROLE_CREDIT_SECRET"
    # response_create_user = api_client.create_user(admin_token, random_username, role)
    # username = response_create_user.username
    #
    # """Аутентификация под кредит-юзером"""
    # response_user_auth = api_client.user_login(username)
    #
    # """Получение токена авторизации для кредит-юзера"""
    # credit_user_token = response_user_auth.token
    #
    # """Создание кредитного счёта"""
    # create_credit_account_response = api_client.create_account(credit_user_token)
    #
    # """Запрос кредита"""
    # credit_acc_id = create_credit_account_response.id
    # credit_amount = 15000
    # term_months = 18
    #
    # request_credit_response = api_client.request_credit(
    #     credit_user_token, credit_acc_id, credit_amount, term_months
    # )
    # #assert request_credit_response.
    #
    # # # assert response_repay_credit.status_code == 200
    # # repay_credit_body = response_repay_credit.json()
    # # assert repay_credit_body.get("amountDeposited") == credit_amount
    # # assert repay_credit_body.get("creditId") == credit_id

    """Аутентификация под кредит-юзером"""
    auth_credit_user_response = api_client.user_login(username)
    assert auth_credit_user_response.status_code == 200
    assert auth_credit_user_response.json().get("token")
    credit_user_token = auth_credit_user_response.json().get("token")

    """Создание счёта для кредит-юзера"""
    create_credit_acc_response = api_client.create_credit_account(credit_user_token)
    assert create_credit_acc_response.status_code == 201
    assert create_credit_acc_response.json().get("balance") == 0

    """Запрос кредита"""
    credit_acc_id = create_credit_acc_response.json().get("id")
    credit_amount = 8888
    term_month = 15

    request_credit_response = api_client.request_credit(
        credit_user_token, credit_acc_id, credit_amount, term_month
    )
    assert request_credit_response.status_code == 201
    credit_body = request_credit_response.json()
    assert credit_body.get("creditId") > 0

    """Погашение кредита"""
    repay_amount = request_credit_response.json().get("amount")
    credit_id = request_credit_response.json().get("creditId")
    response_repay_credit = api_client.repay_credit(
        credit_user_token, credit_id, credit_acc_id, repay_amount
    )
