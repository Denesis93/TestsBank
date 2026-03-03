import allure
import requests
from main.api.models.create_account_response import CreateAccountResponseModel
from src.main.api.requesters.post_base_requester import PostBaseRequester
from http import HTTPStatus

"""Реквестер для создания банковского счёта"""


class CreateAccountPostBaseRequester(PostBaseRequester):
    def post(self, model: None):
        url = f"{self.base_url}/account/create"

        with allure.step(f"POST {url} - создание банковского счёта"):

            # отправка запроса на создание банковского счёта
            response = requests.post(url=url, headers=self.headers)
            allure.attach(
                response.text,
                "Ответ от сервера на запрос создания банковского счёта",
                allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа от сервера"):
            self.response_spec(response)

        with allure.step("Валидация ответа от сервера с помощью Pydantic"):
            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return CreateAccountResponseModel.model_validate(response.json())

            return response.json()
