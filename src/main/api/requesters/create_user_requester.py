import json
import requests
from main.api.models.create_user_response import CreateUserResponseModel
from src.main.api.requesters.post_base_requester import PostBaseRequester
from src.main.api.models.create_user_request import CreateUserRequestModel
from http import HTTPStatus
import allure

"""Реквестер для создания юзера"""


class CreateUserPostBaseRequester(PostBaseRequester):
    def post(self, create_user_request_model: CreateUserRequestModel):
        url = f"{self.base_url}/admin/create"
        headers = self.headers
        payload = create_user_request_model.model_dump()

        with allure.step(f"POST {url} - создание пользователя"):

            # прикрепляю тело запроса (dumps = dump string,
            # это функция, превращающая Python-объект в JSON-строку)
            allure.attach(
                json.dumps(payload, indent=4),
                name="Тело запроса для создания юзера",
                attachment_type=allure.attachment_type.JSON,
            )

            # отправка запроса на создание юзера
            response = requests.post(
                url=url,
                headers=headers,
                json=payload,
            )

            # прикрепляю тело ответа
            allure.attach(
                response.text,
                "Тело ответа после создания юзера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)

        if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
            with allure.step("Валидация ответа с помощью Pydantic"):
                return CreateUserResponseModel.model_validate(response.json())
        return response.json()
