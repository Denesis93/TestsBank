import json
from http import HTTPStatus
import allure
import requests
from main.api.models.repay_credit_response import RepayCreditResponseModel
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.requesters.post_base_requester import PostBaseRequester

"""Реквестер для погашения кредита"""


class RepayCreditPostBaseRequester(PostBaseRequester):
    def post(self, repay_credit_request_model: RequestCreditRequestModel):

        url = f"{self.base_url}/credit/repay"
        payload = repay_credit_request_model.model_dump(by_alias=True)
        with allure.step(f"POST {url} - погашение кредита"):

            # отправка запроса на запрос кредита
            allure.attach(
                json.dumps(payload, indent=4),
                "Тело запроса на погашение кредита",
                attachment_type=allure.attachment_type.JSON,
            )
            response = requests.post(
                url=url,
                headers=self.headers,
                json=payload,
            )
            allure.attach(
                response.text,
                "Тело ответа сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа сервера"):
                return RepayCreditResponseModel.model_validate(response.json())
        return response.json()
