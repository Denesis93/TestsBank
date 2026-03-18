import pytest

from constants import (
    AMOUNT_TO_TRANSFER,
    AMOUNT_DEPOSIT,
    AMOUNT_TO_TRANSFER_INVALID,
    AMOUNT_DEPOSIT_DONOR,
)
from main.api.models.transfer_request import TransferRequestModel
from main.api.requesters.transactions_history_requester import (
    TransactionsHistoryRequester,
)
from main.api.requesters.transfer_requester import TransferPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты для проверки перевода денежных средств"""

@pytest.mark.api
class TestTransfer:
    """Тест перевода денежных средств с валидными данными"""

    def test_transfer_between_own_acc(
        self,
        user_data,
        request_spec_admin,
        create_user,
        request_spec_user,
        create_account_1,
        create_account,
        deposit_account,
    ):
        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id,
            toAccountId=create_account_1.id,
            amount=AMOUNT_TO_TRANSFER,
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
        self,
        user_data,
        request_spec_admin,
        create_user,
        request_spec_user,
        deposit_account,
        create_account,
        create_account_1,
    ):
        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 7777.01
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id,
            toAccountId=create_account_1.id,
            amount=AMOUNT_TO_TRANSFER_INVALID,
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
        create_account,
        create_account_2,
        deposit_account,
    ):
        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 3333.44
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id,
            toAccountId=create_account_2.id,
            amount=AMOUNT_TO_TRANSFER,
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
        create_account,
        create_account_2,
        deposit_account,
    ):
        # тело для запроса на перевод денежных средств
        # Сумма перевода - минимально 500, максимум - 10000
        # amount_to_transfer = 8888.01
        transfer_payload = TransferRequestModel(
            fromAccountId=create_account.id,
            toAccountId=create_account_2.id,
            amount=AMOUNT_TO_TRANSFER_INVALID,
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

    """Тесты проверки истории транзакций при переводе между своими счетами"""

    def test_transactions_history_between_own_accs(
        self,
        user_data,
        request_spec_admin,
        create_user,
        request_spec_user,
        create_account,
        deposit_account,
        create_account_1,
        transfer,
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
            response_history_acceptor.balance
            == create_account_1.balance + AMOUNT_TO_TRANSFER
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
        self,
        user_data,
        request_spec_admin,
        create_user,
        request_spec_user,
        create_account,
        deposit_account,
        create_account_1,
        transfer,
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

    """Тест проверки истории транзакций при переводе средств на счёт другого юзера"""

    def test_transaction_history_between_other_accs(
        self,
        user_data,
        user_2_data,
        request_spec_admin,
        create_user,
        create_user_2,
        request_spec_user,
        request_spec_user_2,
        create_account,
        create_account_2,
        deposit_account,
        transfer_2,
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
            response_history_acceptor.balance
            == create_account_2.balance + AMOUNT_TO_TRANSFER
        )

        # проверка, что в ответе есть хотя бы 1 объект transaction с типом 'transfer_in'

        assert in_transaction is not None
        assert in_transaction.from_account_id == create_account.id
        assert in_transaction.to_account_id == create_account_2.id
        assert in_transaction.amount == AMOUNT_TO_TRANSFER
