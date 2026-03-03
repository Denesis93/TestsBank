import pytest
import random

"""Тест создания кредит-юзера"""


@pytest.mark.api
def test_create_credit_user(api_client, admin_token):
    """Создание кредит-юзера"""
    username = f"Ivan{random.randint(1, 10000)}"
    role = "ROLE_CREDIT_SECRET"
    response_create_user = api_client.create_user(admin_token, username, role)

    assert response_create_user.id > 0
    assert response_create_user.username.startswith("Ivan")
    assert response_create_user.role == "ROLE_CREDIT_SECRET"
