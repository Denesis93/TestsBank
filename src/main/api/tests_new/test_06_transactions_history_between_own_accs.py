import pytest

from constants import AMOUNT_DEPOSIT, AMOUNT_TO_TRANSFER
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.transactions_history_requester import (
    TransactionsHistoryRequester,
)
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты проверки истории транзакций при переводе между своими счетами"""


@pytest.mark.api
class TestTransactionsHistoryBetweenOwnAccs:

    def test_transactions_history_between_own_accs(
        self, user_data, request_spec_admin, create_user, request_spec_user, create_account, deposit_account, create_account_1, transfer
    ):

        """Проверка истории транзакций у донора"""
        # запрос истории транзакций донора
        response_history_donor = TransactionsHistoryRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).get(create_account.id)

        # присваиваю переменной транзакцию, в которой есть транзакции 'transfer_out', т.е., исходящая транзакция (списание денежных средств)
        out_transaction = next(
            (
                transaction
                for transaction in response_history_donor.transactions
                if transaction.type == "transfer_out"
            ),
            None,
        )

        assert response_history_donor.balance == AMOUNT_DEPOSIT - AMOUNT_TO_TRANSFER
        assert response_history_donor.id == create_account.id
        assert out_transaction is not None
        assert out_transaction.from_account_id == create_account.id
        assert out_transaction.to_account_id == create_account_1.id
        assert out_transaction.amount == -AMOUNT_TO_TRANSFER

        """Проверка истории транзакций у приёмника"""
        # запрос истории транзакций приёмника
        response_history_acceptor = TransactionsHistoryRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).get(create_account_1.id)

        # присваиваю переменной транзакцию, в которой есть транзакции 'transfer_in', т.е., входящая транзакция (поступление денежных средств)
        in_transaction = next(
            (
                transaction
                for transaction in response_history_acceptor.transactions
                if transaction.type == "transfer_in"
            ),
            None,
        )

        assert (
            response_history_acceptor.balance == create_account_1.balance + AMOUNT_TO_TRANSFER
        )

        # проверка, что в ответе есть хотя бы 1 объект transaction с типом 'transfer_in'
        assert any(
            transaction.type == "transfer_in"
            for transaction in response_history_acceptor.transactions
        ), 'Типа транзакции "transfer_in" не найдено'

        assert in_transaction is not None
        assert in_transaction.from_account_id == create_account.id
        assert in_transaction.to_account_id == create_account_1.id
        assert in_transaction.amount == AMOUNT_TO_TRANSFER


    """Тест проверки истории транзакций у несуществующего банковского счёта"""

    def test_transactions_history_between_own_accs_invalid(
        self, user_data, request_spec_admin, create_user, request_spec_user, create_account, deposit_account, create_account_1, transfer
    ):


        """Проверка истории транзакций у донора"""
        # запрос истории транзакций донора
        response_history_donor = TransactionsHistoryRequester(
            request_spec=request_spec_user,
            response_spec=ResponseSpecs.not_found_status(),
        ).get(acc_id=123)

        assert (
            response_history_donor["error"]
            == f"Account {123} not found or does not belong to userId {create_user.id}"
        )
