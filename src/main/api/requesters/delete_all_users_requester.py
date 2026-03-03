import json
from http import HTTPStatus
import allure
import requests
from main.api.models.delete_all_users_response_model import DeleteAllUsersResponseModel
from main.api.requesters.base_requester import BaseRequester

"""Реквестер для удаления всех юзеров"""


class DeleteAllUsersRequester(BaseRequester):
    def delete_all(self):
        url = f"{self.base_url}/admin/users"
        headers = self.headers

        with allure.step(f"DELETE {url} - удаление всех юзеров"):

            # прикрепляю отправляемые данные при запросе на удаление всех юзеров
            allure.attach(
                json.dumps(
                    {"url": url, "method": "DELETE", "headers": headers}, indent=4
                ),
                name="Тело запроса на удаление всех юзеров",
                attachment_type=allure.attachment_type.JSON,
            )

            response = requests.delete(url=url, headers=headers)

            # прикрепляю ответ от сервера
            allure.attach(
                response.text,
                "Тело ответа от сервера после удаления всех юзеров",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа с помощью Pydantic"):
                return DeleteAllUsersResponseModel.model_validate(response.json())
        return response
