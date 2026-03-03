from http import HTTPStatus
import allure
import requests
from main.api.models.delete_one_user_response_model import DeleteOneUserResponseModel
from main.api.requesters.base_requester import BaseRequester

"""Реквестер для удаления одного юзера"""


class DeleteOneUserRequester(BaseRequester):
    def delete_one(self, user_id: int):
        url = f"{self.base_url}/admin/users/{user_id}"
        with allure.step(f"DELETE {url} - удаление юзера"):

            # отправка запроса на удаление юзера
            response = requests.delete(url=url, headers=self.headers)

            allure.attach(
                response.text,
                "Ответ сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа сервера с помощью Pydantic"):
                return DeleteOneUserResponseModel.model_validate(response.json())
        return response.json()
