import pytest
from constants import AMOUNT_DEPOSIT_DONOR, AMOUNT_TO_TRANSFER, AMOUNT_TO_TRANSFER_INVALID
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты перевода денежных средств на чужой банковский счёт"""


@pytest.mark.api
class TestTransferToOtherAcc:

    """Тест перевода денежных средств на чужой банковский счёт с валидными данными"""

    def test_transfer_to_other_acc(
        self,
        user_data,
        user_2_data,
        request_spec_admin,
        create_user,
        create_user_2,
        request_spec_user,
        request_spec_user_2,
    create_account, create_account_2, deposit_account):


        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 3333.44
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_2.id, amount=AMOUNT_TO_TRANSFER
        )

        # отправка запроса на перевод денежных средств
        transfer_response = TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(transfer_payload)

        assert transfer_response.from_account_id == create_account.id
        assert transfer_response.to_account_id == create_account_2.id
        assert (
            transfer_response.from_account_id_balance
            == AMOUNT_DEPOSIT_DONOR - AMOUNT_TO_TRANSFER
        )

    """Тест перевода денежных средств на чужой банковский счёт с невалидными данными (перевод больше, чем имеется денежных средств на счету)"""

    def test_transfer_to_other_acc_invalid(
        self,
        user_data,
        user_2_data,
        request_spec_admin,
        create_user,
        create_user_2,
        request_spec_user,
        request_spec_user_2,
    create_account, create_account_2, deposit_account):

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 8888.01
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id, toAccountId=create_account_2.id, amount=AMOUNT_TO_TRANSFER_INVALID
        )

        # отправка запроса на перевод денежных средств
        transfer_response = TransferPostBaseRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.unprocessable_status(),
        ).post(transfer_payload)

        assert (
            transfer_response["error"]
            == f"Insufficient funds. Current balance: {deposit_account.balance:.2f}, required: {AMOUNT_TO_TRANSFER_INVALID}"
        )
