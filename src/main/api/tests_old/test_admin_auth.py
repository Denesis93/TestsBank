import pytest

"""Тест аутентификации под админом"""


@pytest.mark.api
def test_admin_auth(api_client):
    """Аутентификация под админом"""
    token = api_client.get_admin_token()
    assert token
