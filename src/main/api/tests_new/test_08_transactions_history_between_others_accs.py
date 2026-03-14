import pytest

from constants import AMOUNT_DEPOSIT_DONOR, AMOUNT_TO_TRANSFER
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.deposit_requester import DepositPostBaseRequester
from main.api.requesters.transactions_history_requester import TransactionsHistoryRequester
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тест проверки истории транзакций при переводе средств на счёт другого юзера"""


@pytest.mark.api
class TestTransactionHistoryBetweenOtherAccs:

    def test_transaction_history_between_other_accs(
        self, user_data,
        user_2_data,
        request_spec_admin,
        create_user,
        create_user_2,
        request_spec_user,
        request_spec_user_2,
    create_account, create_account_2, deposit_account, transfer_2
    ):

        # # отправка запроса на создание банковского счёта №1 (донор)
        # response_create_account_donor = CreateAccountPostBaseRequester(
        #     request_spec=request_spec_user,
        #     response_spec=ResponseSpecs.created_status(),
        # ).post(None)
        #
        # # получение айдишника счёта донора
        # donor_id = response_create_account_donor.id
        #
        # # отправка запроса на создание банковского счёта №2 (приёмник)
        # response_create_account_acceptor = CreateAccountPostBaseRequester(
        #     request_spec=request_spec_user_2,
        #     response_spec=ResponseSpecs.created_status(),
        # ).post(None)
        #
        # # получение айдишника счёта приёмника
        # acceptor_id = response_create_account_acceptor.id
        #
        # # получение баланса приёмника
        # balance_acceptor = response_create_account_acceptor.balance
        #
        # # тело для запроса на пополнение счёта донора
        # # Сумма пополнения (deposit) - минимально 1000, максимально - 9000
        #
        # amount_deposit_donor = 8888
        # payload_deposit_donor = DepositRequestModel(
        #     accountId=donor_id, amount=amount_deposit_donor
        # )
        #
        # # отправка запроса на пополнение счёта донора
        # DepositPostBaseRequester(
        #     request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        # ).post(payload_deposit_donor)
        #
        # # тело для запроса на перевод денежных средств
        # # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 3333.44
        # transfer_payload = TransferRequestModel(
        #     fromAccountId=donor_id, toAccountId=acceptor_id, amount=amount_to_transfer
        # )
        #
        # # отправка запроса на перевод денежных средств
        # transfer_response = TransferPostBaseRequester(
        #     request_spec=request_spec_user, response_spec=ResponseSpecs.ok_status()
        # ).post(transfer_payload)

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

        assert response_history_donor.balance == round(
            AMOUNT_DEPOSIT_DONOR - AMOUNT_TO_TRANSFER, 2
        )
        assert response_history_donor.id == create_account.id
        assert out_transaction is not None
        assert out_transaction.from_account_id == create_account.id
        assert out_transaction.to_account_id == create_account_2.id
        assert out_transaction.amount == -AMOUNT_TO_TRANSFER


        """Проверка истории транзакций у приёмника"""
        # запрос истории транзакций приёмника
        response_history_acceptor = TransactionsHistoryRequester(
            request_spec=request_spec_user_2, response_spec=ResponseSpecs.ok_status()
        ).get(create_account_2.id)

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
            response_history_acceptor.balance == create_account_2.balance + AMOUNT_TO_TRANSFER
        )

        # проверка, что в ответе есть хотя бы 1 объект transaction с типом 'transfer_in'

        assert in_transaction is not None
        assert in_transaction.from_account_id == create_account.id
        assert in_transaction.to_account_id == create_account_2.id
        assert in_transaction.amount == AMOUNT_TO_TRANSFER
