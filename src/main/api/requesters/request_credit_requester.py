import json
from http import HTTPStatus
import allure
import requests
from main.api.models.request_credit_request import RequestCreditRequestModel
from main.api.models.request_credit_response import RequestCreditResponseModel
from main.api.requesters.post_base_requester import PostBaseRequester

"""Реквестер для запроса кредита"""


class CreditPostBaseRequester(PostBaseRequester):
    def post(self, request_credit_model: RequestCreditRequestModel):
        payload = request_credit_model.model_dump(by_alias=True)
        url = f"{self.base_url}/credit/request"
        with allure.step(f"POST {url} - запрос кредита"):
            allure.attach(
                json.dumps(payload, indent=4),
                "Тело запроса на запрос кредита",
                attachment_type=allure.attachment_type.JSON,
            )
            # отправка запроса на запрос кредита
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

        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            with allure.step("Валидация ответа сервера"):
                return RequestCreditResponseModel.model_validate(response.json())
        return response.json()
