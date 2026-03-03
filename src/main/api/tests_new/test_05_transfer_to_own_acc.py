import pytest
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты перевода денежных средств на свой банковский счёт"""


@pytest.mark.api
class TestTransferToOwnAcc:
    """Тест перевода денежных средств с валидными данными"""

    def test_transfer_between_own_acc(
        self, user_data, request_spec_admin, create_user, request_spec_user
    ):

        # отправка запроса на создание банковского счёта №1 (донор)
        response_create_account_donor = CreateAccountPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.created_status()
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        donor_id = response_create_account_donor.id
        amount_deposit = 7777
        payload_deposit = DepositRequestModel(accountId=donor_id, amount=amount_deposit)

        # отправка запроса на пополнение счёта донора
        DepositPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(payload_deposit)

        # отправка запроса на создание банковского счёта №2 (приёмник)
        response_create_account_acceptor = CreateAccountPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.created_status()
        ).post(None)

        # получение айдишника приёмника
        acceptor_id = response_create_account_acceptor.id

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        amount_to_transfer = 6666
        transfer_payload = TransferRequestModel(
            fromAccountId=donor_id, toAccountId=acceptor_id, amount=amount_to_transfer
        )

        # отправка запроса на перевод денежных средств
        transfer_response = TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(transfer_payload)

        assert transfer_response.from_account_id == donor_id
        assert transfer_response.to_account_id == acceptor_id
        assert (
            transfer_response.from_account_id_balance
            == amount_deposit - amount_to_transfer
        )

    """Тест перевода денежных средств с невалидными данными (перевод больше, чем имеется денежных средств на счету)"""

    # @pytest.mark.parametrize('amount_to_transfer', [])

    def test_transfer_between_own_acc_invalid(
        self, user_data, request_spec_admin, create_user, request_spec_user
    ):
        # отправка запроса на создание банковского счёта №1 (донор)
        response_create_account_donor = CreateAccountPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.created_status()
        ).post(None)

        # тело для запроса на пополнение счёта
        # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        donor_id = response_create_account_donor.id
        amount_deposit = 7777
        payload_deposit = DepositRequestModel(accountId=donor_id, amount=amount_deposit)

        # отправка запроса на пополнение счёта донора
        deposit_donor_response = DepositPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(payload_deposit)

        # отправка запроса на создание банковского счёта №2 (приёмник)
        response_create_account_acceptor = CreateAccountPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.created_status()
        ).post(None)

        # получение айдишника приёмника
        acceptor_id = response_create_account_acceptor.id

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        amount_to_transfer = 7777.01
        transfer_payload = TransferRequestModel(
            fromAccountId=donor_id, toAccountId=acceptor_id, amount=amount_to_transfer
        )

        # отправка запроса на перевод денежных средств
        transfer_response = TransferPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.unprocessable_status(),
        ).post(transfer_payload)

        # использую форматирование .2f, т.к. сервер возвращает значение deposit_donor_response.balance с двумя нулями,
        # а python форматирует с одним нулём (7777.00 - сервер, 7777.0 - питон)
        assert (
            transfer_response["error"]
            == f"Insufficient funds. Current balance: {deposit_donor_response.balance:.2f}, required: {amount_to_transfer}"
        )
