import pytest
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

        # получение баланса приёмника
        balance_acceptor = response_create_account_acceptor.balance

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        amount_to_transfer = 6666
        transfer_payload = TransferRequestModel(
            fromAccountId=donor_id, toAccountId=acceptor_id, amount=amount_to_transfer
        )

        # отправка запроса на перевод денежных средств
        TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(transfer_payload)

        """Проверка истории транзакций у донора"""
        # запрос истории транзакций донора
        response_history_donor = TransactionsHistoryRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).get(donor_id)

        # присваиваю переменной транзакцию, в которой есть транзакции 'transfer_out', т.е., исходящая транзакция (списание денежных средств)
        out_transaction = next(
            (
                transaction
                for transaction in response_history_donor.transactions
                if transaction.type == "transfer_out"
            ),
            None,
        )

        assert response_history_donor.balance == amount_deposit - amount_to_transfer
        assert response_history_donor.id == donor_id
        assert out_transaction is not None
        assert out_transaction.from_account_id == donor_id
        assert out_transaction.to_account_id == acceptor_id
        assert out_transaction.amount == -amount_to_transfer

        """Проверка истории транзакций у приёмника"""
        # запрос истории транзакций приёмника
        response_history_acceptor = TransactionsHistoryRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).get(acceptor_id)

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
            response_history_acceptor.balance == balance_acceptor + amount_to_transfer
        )

        # проверка, что в ответе есть хотя бы 1 объект transaction с типом 'transfer_in'
        assert any(
            transaction.type == "transfer_in"
            for transaction in response_history_acceptor.transactions
        ), 'Типа транзакции "transfer_in" не найдено'

        assert in_transaction is not None
        assert in_transaction.from_account_id == donor_id
        assert in_transaction.to_account_id == acceptor_id
        assert in_transaction.amount == amount_to_transfer

    """Тест проверки истории транзакций у несуществующего банковского счёта"""

    def test_transactions_history_between_own_accs_invalid(
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

        # получение баланса приёмника
        balance_acceptor = response_create_account_acceptor.balance

        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        amount_to_transfer = 6666
        transfer_payload = TransferRequestModel(
            fromAccountId=donor_id, toAccountId=acceptor_id, amount=amount_to_transfer
        )

        # отправка запроса на перевод денежных средств
        TransferPostBaseRequester(
            request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        ).post(transfer_payload)

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
