import pytest
from constants import AMOUNT_DEPOSIT, CREDIT_AMOUNT, TERM_MONTHS, REPAY_AMOUNT
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.models.repay_credit_request import RepayCreditRequestModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.login_user_requester import LoginUserPostBaseRequester
from main.api.requesters.repay_credit_requester import RepayCreditPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""Тесты для кредита"""


@pytest.mark.api
class TestCredit:
    """Тест создания кредитного юзера с валидными данными"""

    def test_create_credit_user(
        self, credit_user_data, request_spec_admin, payload_create_credit_user
    ):

        # отправка запроса на создание кредитного юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).post(payload_create_credit_user)

        assert response_create_user.role == credit_user_data["role"]
        assert response_create_user.id > 0
        assert response_create_user.username == credit_user_data["username"]

    """Тест логина кредитного юзера с валидными данными"""

    def test_credit_user_login(self, create_credit_user, credit_user_data):
        # тело для запроса на логин кредитного пользователя
        payload_credit_user_login = LoginUserRequestModel(
            username=credit_user_data["username"], password=credit_user_data["password"]
        )

        # отправка запроса на логин кредитного пользователя
        response_credit_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_credit_user_login)

        assert response_credit_user_login.user.username == credit_user_data["username"]
        assert response_credit_user_login.user.role == credit_user_data["role"]
        assert response_credit_user_login.token

    """Тест создания кредитного банковского счёта с валидными данными"""

    def test_create_credit_account(self, create_credit_user, request_spec_credit_user):

        # отправка запроса на создание кредитного аккаунта
        response_create_credit_account = CreateAccountPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(None)

        assert response_create_credit_account.id > 0
        assert response_create_credit_account.balance == 0
        assert response_create_credit_account.number

    """Тест пополнения кредитного счёта валидными данными"""

    def test_deposit_credit_acc(
        self, create_credit_user, request_spec_credit_user, create_credit_account
    ):
        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        payload_deposit = DepositRequestModel(
            accountId=create_credit_account.id, amount=AMOUNT_DEPOSIT
        )

        # отправка запроса на пополнение счёта
        response_deposit = DepositPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_deposit)

        assert response_deposit.balance == AMOUNT_DEPOSIT
        assert response_deposit.id == create_credit_account.id

    """Тест запроса кредита с валидными данными"""

    def test_request_credit(
        self, create_credit_user, request_spec_credit_user, create_credit_account
    ):
        # тело запроса на получение кредита
        payload_request_credit = RequestCreditRequestModel(
            accountId=create_credit_account.id,
            amount=CREDIT_AMOUNT,
            termMonths=TERM_MONTHS,
        )

        # отправка запроса на получение кредита
        response_request_credit = CreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.created_status(),
        ).post(payload_request_credit)

        assert response_request_credit.id > 0
        assert response_request_credit.credit_id > 0
        assert response_request_credit.amount == CREDIT_AMOUNT
        assert response_request_credit.term_months == TERM_MONTHS
        assert response_request_credit.balance == CREDIT_AMOUNT

    """Тест погашения кредита с валидными данными"""

    def test_repay_credit(
        self,
        create_credit_user,
        request_spec_credit_user,
        create_credit_account,
        deposit_credit_account,
        request_credit,
    ):
        # тело запроса на погашение кредита

        payload_repay_credit = RepayCreditRequestModel(
            creditId=request_credit.credit_id,
            accountId=create_credit_account.id,
            amount=CREDIT_AMOUNT,
        )

        # отправка запроса на погашение кредита
        response_repay_credit = RepayCreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_repay_credit)

        assert response_repay_credit.creditId == request_credit.credit_id
        assert response_repay_credit.amount_deposited == REPAY_AMOUNT
