from http import HTTPStatus
import allure
import requests
from main.api.models.transaction_history_response import (
    TransactionsHistoryResponseModel,
)
from main.api.requesters.base_requester import BaseRequester

"""Реквестер для получения истории транзакций"""


class TransactionsHistoryRequester(BaseRequester):
    def get(self, acc_id: int):
        url = f"{self.base_url}/account/transactions/{acc_id}"
        with allure.step(
            f"GET {url} - получение истории транзакций для указанного счета"
        ):
            response = requests.get(url=url, headers=self.headers)
            allure.attach(
                response.text,
                "Тело ответа от сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа сервера"):
            self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа сервера"):
                return TransactionsHistoryResponseModel.model_validate(response.json())
        return response.json()
