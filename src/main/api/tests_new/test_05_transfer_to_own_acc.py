import pytest
from constants import AMOUNT_DEPOSIT, AMOUNT_TO_TRANSFER, AMOUNT_TO_TRANSFER_INVALID
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

    def test_transfer_between_own_acc(self, user_data, request_spec_admin, create_user, request_spec_user, create_account_1, create_account, deposit_account):

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_1.id, amount=AMOUNT_TO_TRANSFER
        )

        # отправка запроса на перевод денежных средств
        transfer_response = TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(transfer_payload)

        assert transfer_response.from_account_id == create_account.id
        assert transfer_response.to_account_id == create_account_1.id
        assert (
            transfer_response.from_account_id_balance
            == AMOUNT_DEPOSIT - AMOUNT_TO_TRANSFER
        )

    """Тест перевода денежных средств с невалидными данными (перевод больше, чем имеется денежных средств на счету)"""

    # @pytest.mark.parametrize('amount_to_transfer', [])

    def test_transfer_between_own_acc_invalid(
        self, user_data, request_spec_admin, create_user, request_spec_user, deposit_account, create_account, create_account_1
    ):

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        #amount_to_transfer = 7777.01
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_1.id, amount=AMOUNT_TO_TRANSFER_INVALID
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
            == f"Insufficient funds. Current balance: {deposit_account.balance:.2f}, required: {AMOUNT_TO_TRANSFER_INVALID}"
        )
