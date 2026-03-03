import json
from http import HTTPStatus
import allure
import requests
from main.api.models.admin_login_request import AdminLoginRequestModel
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.models.login_user_response import LoginUserResponseModel
from main.api.requesters.post_base_requester import PostBaseRequester

"""Реквестер для логина"""


class LoginUserPostBaseRequester(PostBaseRequester):
    def post(
        self, login_user_request_model: LoginUserRequestModel | AdminLoginRequestModel
    ):
        payload = login_user_request_model.model_dump()
        url = f"{self.base_url}/auth/token/login"

        with allure.step(f"POST {url} - Логин"):
            # форматирую JSON для красивого отображения в отчёте Allure
            allure.attach(
                json.dumps(payload, indent=4),
                "Тело запроса на логин",
                attachment_type=allure.attachment_type.JSON,
            )
            # отправка запроса на логин юзера
            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
            )
            allure.attach(
                response.text,
                "Ответ сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа сервера"):
            self.response_spec(response)
        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа сервера"):
                response_model = LoginUserResponseModel.model_validate(response.json())
            return response_model
        return response.json()
