import requests
from src.main.api.models.admin_login_request import AdminLoginRequestModel
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.models.admin_login_response import AdminLoginResponseModel
from src.main.api.models.create_user_request import CreateUserRequestModel
from src.main.api.models.create_user_response import CreateUserResponseModel
from src.main.api.models.login_user_request import LoginUserRequestModel
from src.main.api.models.login_user_response import LoginUserResponseModel
from src.main.api.models.create_account_response import CreateAccountResponseModel
from src.main.api.models.deposit_request import DepositRequestModel
from src.main.api.models.deposit_response import DepositResponseModel
from src.main.api.models.transfer_request import TransferRequestModel
from src.main.api.models.transfer_response import TransferResponseModel
from src.main.api.models.request_credit_request import RequestCreditRequestModel
from src.main.api.models.request_credit_response import RequestCreditResponseModel
from src.main.api.models.repay_credit_request import RepayCreditRequestModel
from src.main.api.models.repay_credit_response import RepayCreditResponseModel
from src.main.api.models.transaction_history_response import (
    TransactionsHistoryResponseModel,
)


class ApiClient:
    def __init__(self, base_url):
        self.base_url = base_url

    """Логин под админом"""

    def get_admin_token(self):

        headers = RequestSpecs.base_headers()
        admin_login_request = AdminLoginRequestModel(
            username="admin", password="123456"
        )
        response = requests.post(
            f"{self.base_url}/auth/token/login",
            json=admin_login_request.model_dump(),
            headers=headers,
        )
        assert response.status_code == 200
        admin_login_response = AdminLoginResponseModel.model_validate(response.json())
        admin_token = admin_login_response.token
        return admin_token

    """Создание юзера"""

    def create_user(self, admin_token, username, role):
        headers = RequestSpecs.auth_headers(admin_token)
        payload_user_create = CreateUserRequestModel(
            username=username, password="Pas!sw0rd", role=role
        )

        response = requests.post(
            f"{self.base_url}/admin/create",
            json=payload_user_create.model_dump(),
            headers=headers,
        )
        assert (
            response.status_code == 200
        ), f"Actual statuscode is {response.status_code}"
        create_user_response = CreateUserResponseModel.model_validate(response.json())
        return create_user_response

    """Создание юзера без модели (для негатива)"""

    def create_user_raw(self, admin_token, username, role):
        headers = RequestSpecs.auth_headers(admin_token)
        payload_user_create = CreateUserRequestModel(
            username=username, password="Pas!sw0rd", role=role
        )

        response = requests.post(
            f"{self.base_url}/admin/create",
            json=payload_user_create.model_dump(),
            headers=headers,
        )
        return response

    """Аутентифицируемся под юзером"""

    def user_login(self, username):
        headers = RequestSpecs.base_headers()
        payload_user_auth = LoginUserRequestModel(
            username=username, password="Pas!sw0rd"
        )

        response = requests.post(
            f"{self.base_url}/auth/token/login",
            json=payload_user_auth.model_dump(),
            headers=headers,
        )
        assert (
            response.status_code == 200
        ), f"Actual statuscode is {response.status_code}"
        login_user_response = LoginUserResponseModel.model_validate(response.json())
        return login_user_response

    """Создание банковского счёта"""

    def create_account(self, user_token):
        headers = RequestSpecs.auth_headers(user_token)
        response = requests.post(f"{self.base_url}/account/create", headers=headers)
        assert (
            response.status_code == 201
        ), f"Actual statuscode is {response.status_code}"
        create_account_response = CreateAccountResponseModel.model_validate(
            response.json()
        )
        return create_account_response

    """Создание банковского счёта без модели (для негатива)"""

    def create_account_raw(self, user_token):
        headers = RequestSpecs.auth_headers(user_token)
        response = requests.post(f"{self.base_url}/account/create", headers=headers)
        return response

    """Пополнение банковского счёта"""

    def deposit(self, user_token, acc_id, amount):
        headers = RequestSpecs.auth_headers(user_token)
        payload_deposit = DepositRequestModel(accountId=acc_id, amount=amount)

        response = requests.post(
            f"{self.base_url}/account/deposit",
            headers=headers,
            json=payload_deposit.model_dump(
                by_alias=True
            ),  # чтоб передавать по алиасу accountId, а не как в модели account_id
        )
        assert (
            response.status_code == 200
        ), f"Actual statuscode is {response.status_code}"
        response_deposit = DepositResponseModel.model_validate(response.json())
        return response_deposit

    """Пополнение банковского счёта без модели (для негатива)"""

    def deposit_raw(self, user_token, acc_id, amount):
        headers = RequestSpecs.auth_headers(user_token)
        payload_deposit = DepositRequestModel(accountId=acc_id, amount=amount)

        response = requests.post(
            f"{self.base_url}/account/deposit",
            headers=headers,
            json=payload_deposit.model_dump(by_alias=True),
        )
        return response

    """Перевод денежных средств на другой счёт"""

    def transfer(self, id_donor, id_acceptor, user_token, amount):
        headers = RequestSpecs.auth_headers(user_token)
        payload_transfer = TransferRequestModel(
            fromAccountId=id_donor, toAccountId=id_acceptor, amount=amount
        )

        response = requests.post(
            f"{self.base_url}/account/transfer",
            headers=headers,
            json=payload_transfer.model_dump(by_alias=True),
        )
        assert (
            response.status_code == 200
        ), f"Actual status code is {response.status_code}"
        response_transfer = TransferResponseModel.model_validate(response.json())
        return response_transfer

    """Перевод денежных средств на другой счёт без модели (для негатива)"""

    def transfer_raw(self, id_donor, id_acceptor, user_token, amount):
        headers = RequestSpecs.auth_headers(user_token)
        payload_transfer = TransferRequestModel(
            fromAccountId=id_donor, toAccountId=id_acceptor, amount=amount
        )

        response = requests.post(
            f"{self.base_url}/account/transfer",
            headers=headers,
            json=payload_transfer.model_dump(by_alias=True),
        )
        return response

    """Получение истории транзакций для указанного счета"""

    def get_transactions_history(self, user_token, acc_id):
        headers = RequestSpecs.auth_headers(user_token)
        response = requests.get(
            f"{self.base_url}/account/transactions/{acc_id}", headers=headers
        )
        assert response.status_code == 200
        transaction_history_response = TransactionsHistoryResponseModel.model_validate(
            response.json()
        )
        return transaction_history_response

    """Запрос кредита"""

    def request_credit(self, credit_user_token, credit_acc_id, amount, term_month):
        headers = RequestSpecs.auth_headers(token=credit_user_token)
        payload_credit = RequestCreditRequestModel(
            accountId=credit_acc_id, amount=amount, termMonths=term_month
        )

        response = requests.post(
            f"{self.base_url}/credit/request",
            headers=headers,
            json=payload_credit.model_dump(by_alias=True),
        )
        assert (
            response.status_code == 201
        ), f"Actual statuscode is {response.status_code}"
        request_credit_response = RequestCreditResponseModel.model_validate(
            response.json()
        )
        return request_credit_response

    """Запрос кредита без модели (для негатива)"""

    def request_credit_raw(self, credit_user_token, credit_acc_id, amount, term_month):
        headers = RequestSpecs.auth_headers(token=credit_user_token)
        payload_credit = RequestCreditRequestModel(
            accountId=credit_acc_id, amount=amount, termMonths=term_month
        )
        response_request_credit = requests.post(
            f"{self.base_url}/credit/request",
            headers=headers,
            json=payload_credit.model_dump(by_alias=True),
        )
        return response_request_credit

    """Погашение кредита"""

    def repay_credit(self, credit_user_token, credit_id, acc_id, amount):
        headers = RequestSpecs.auth_headers(credit_user_token)

        payload_repay_credit = RepayCreditRequestModel(
            creditId=credit_id, accountId=acc_id, amount=amount
        )

        response = requests.post(
            f"{self.base_url}/credit/repay",
            headers=headers,
            json=payload_repay_credit,
        )
        assert (
            response.status_code == 200
        ), f"Actual statuscode is {response.status_code}"
        response_repay_credit = RepayCreditResponseModel.model_validate(response.json())
        return response_repay_credit
