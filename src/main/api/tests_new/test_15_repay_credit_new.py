import pytest

from constants import CREDIT_AMOUNT, REPAY_AMOUNT, REPAY_AMOUNT_INVALID
from main.api.models.repay_credit_request import RepayCreditRequestModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.create_account_requester import CreateAccountPostBaseRequester
from main.api.requesters.repay_credit_requester import RepayCreditPostBaseRequester
from main.api.requesters.request_credit_requester import CreditPostBaseRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты погашения кредита"""


@pytest.mark.api
class TestRequestCredit:
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

    """Тест погашения кредита с невалидными данными (погашение на недостаточную сумму)"""

    def test_repay_credit_invalid(
        self,
        create_credit_user,
        request_spec_credit_user,
        create_credit_account,
        request_credit,
    ):

        # тело запроса на погашение кредита
        payload_repay_credit = RepayCreditRequestModel(
            creditId=request_credit.credit_id,
            accountId=create_credit_account.id,
            amount=REPAY_AMOUNT_INVALID,
        )

        # отправка запроса на погашение кредита с недостаточной суммой для погашения
        response_repay_credit = RepayCreditPostBaseRequester(
            request_spec=request_spec_credit_user,
            response_spec=ResponseSpecs.unprocessable_status(),
        ).post(payload_repay_credit)

        assert (
            response_repay_credit["error"]
            == f"The amount is not enough. Credit balance: -{request_credit.balance:.0f}"
        )
