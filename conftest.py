import random
import pytest
import names
from constants import AMOUNT_DEPOSIT, AMOUNT_TO_TRANSFER, CREDIT_AMOUNT, TERM_MONTHS
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""""Фиктсуры для обычного пользователя""" ""

"""Данные для обычного пользователя"""

@pytest.fixture
def user_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 1000)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_USER",
    }


"""Данные для обычного 2го пользователя (для тестов, где нужно создавать 2х разных юзеров)"""

@pytest.fixture
def user_2_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 1000)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_USER",
    }


"""Реквест-спек для админа"""

@pytest.fixture
def request_spec_admin():
    return RequestSpecs.login_and_get_request_spec("admin", "123456")


"""Тело для запроса на создание обычного юзера"""

@pytest.fixture
def payload_create_user(user_data):
    return CreateUserRequestModel(
        username=user_data["username"],
        password=user_data["password"],
        role=user_data["role"],
    )


"""Тело для запроса на создание обычного юзера 2"""

@pytest.fixture
def payload_create_user_2(user_2_data):
    return CreateUserRequestModel(
        username=user_2_data["username"],
        password=user_2_data["password"],
        role=user_2_data["role"],
    )


"""Создание обычного пользователя"""

@pytest.fixture
def create_user(user_data, payload_create_user, request_spec_admin):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_user)


"""Создание обычного пользователя 2"""

@pytest.fixture
def create_user_2(user_2_data, payload_create_user_2, request_spec_admin):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_user_2)


"""Реквест-спек для обычного юзера"""

@pytest.fixture
def request_spec_user(user_data):
    username = user_data["username"]
    password = user_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)


"""Реквест-спек для юзера 2"""

@pytest.fixture
def request_spec_user_2(user_2_data):
    username = user_2_data["username"]
    password = user_2_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)



"""Фикстуры для создания банковского счёта"""



"""Создание банковского счёта №1"""

@pytest.fixture
def create_account(request_spec_user):
    return CreateAccountPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

"""Создание банковского счёта №2 (тем же юзером)"""

@pytest.fixture
def create_account_1(request_spec_user):
    return CreateAccountPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)


"""Создание банковского счёта №2 (другим юзером)"""

@pytest.fixture
def create_account_2(request_spec_user_2):
    return CreateAccountPostBaseRequester(
            request_spec=request_spec_user_2,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)



"""Фикстуры для пополнения банковского счёта"""


"""Тело для пополнения счёта"""

@pytest.fixture
def payload_deposit(create_account):
    return DepositRequestModel(accountId=create_account.id, amount=AMOUNT_DEPOSIT)


"""Пополнение счёта"""

@pytest.fixture
def deposit_account(request_spec_user, payload_deposit):
    return DepositPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(payload_deposit)


"""Тело для перевода денежных средств на счёт того же пользователя"""

@pytest.fixture
def payload_transfer(create_account, create_account_1):
    return TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_1.id, amount=AMOUNT_TO_TRANSFER)


"""Перевод денежных средств на счёт того же пользователя"""
@pytest.fixture
def transfer(request_spec_user, payload_transfer):
    return  TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(payload_transfer)


"""Тело для перевода денежных средств на счёт другого пользователя"""

@pytest.fixture
def payload_transfer_2(create_account, create_account_2):
    return TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_2.id, amount=AMOUNT_TO_TRANSFER)


"""Перевод денежных средств на счёт другого пользователя"""

@pytest.fixture
def transfer_2(request_spec_user, payload_transfer_2, deposit_account):
    return  TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(payload_transfer_2)







"""""Фиктсуры для кредитного пользователя""" ""

"""Данные для кредитного пользователя"""


@pytest.fixture
def credit_user_data():
    return {
        "username": f"{names.get_first_name()}{random.randint(1, 100)}",
        "password": "Pas!sw0rd",
        "role": "ROLE_CREDIT_SECRET",
    }


"""Тело для запроса на создание кредитного юзера"""

@pytest.fixture
def payload_create_credit_user(credit_user_data):
    return CreateUserRequestModel(
        username=credit_user_data["username"],
        password=credit_user_data["password"],
        role=credit_user_data["role"],
    )


"""Создание кредитного пользователя"""

@pytest.fixture
def create_credit_user(
    credit_user_data, payload_create_credit_user, request_spec_admin
):
    # отправка запроса на создание юзера
    return CreateUserPostBaseRequester(
        request_spec=request_spec_admin,
        response_spec=ResponseSpecs.ok_status(),
    ).post(payload_create_credit_user)


"""Реквест-спек для кредитного юзера"""


@pytest.fixture
def request_spec_credit_user(credit_user_data):
    username = credit_user_data["username"]
    password = credit_user_data["password"]
    return RequestSpecs.login_and_get_request_spec(username=username, password=password)



"""Создание кредитного банковского счёта"""

@pytest.fixture
def create_credit_account(request_spec_credit_user):
    return CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)



"""Тело для пополнения кредитного счёта"""

@pytest.fixture
def payload_deposit_credit_acc(create_credit_account):
    # тело для запроса на пополнение счёта
    # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
    return DepositRequestModel(accountId=create_credit_account.id, amount=AMOUNT_DEPOSIT)


"""Пополнение кредитного счёта"""

@pytest.fixture
def deposit_credit_account(request_spec_credit_user, payload_deposit_credit_acc):
        # отправка запроса на пополнение счёта
        return DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit_credit_acc)


"""Тело для запроса кредита"""

@pytest.fixture
def payload_request_credit(create_credit_account):
    return RequestCreditRequestModel(
        accountId=create_credit_account.id, amount=CREDIT_AMOUNT, termMonths=TERM_MONTHS
    )


"""Запрос кредита"""

@pytest.fixture
def request_credit(request_spec_credit_user, payload_request_credit):
    return CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)









