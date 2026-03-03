import allure
import requests
from main.api.models.deposit_request import DepositRequestModel
from main.api.models.deposit_response import DepositResponseModel
from main.api.requesters.post_base_requester import PostBaseRequester
from http import HTTPStatus

"""Реквестер для пополнения банковского счёта"""


class DepositPostBaseRequester(PostBaseRequester):
    def post(self, deposit_request_model: DepositRequestModel):
        url = f"{self.base_url}/account/deposit"
        payload = deposit_request_model.model_dump(by_alias=True)

        with allure.step(f"POST {url} - пополнение счёта"):
            allure.attach(
                str(payload),
                "Тело запроса",
                attachment_type=allure.attachment_type.JSON,
            )

            # отправка запроса на пополнение банковского счёта
            response = requests.post(url=url, headers=self.headers, json=payload)
            allure.attach(
                response.text,
                "Тело ответа от сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа с помощью Pydantic"):
                return DepositResponseModel.model_validate(response.json())
        return response.json()
