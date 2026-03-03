import allure
import requests
from main.api.requesters.base_requester import BaseRequester

"""Реквестер для получения списка юзеров"""


class GetUsersRequester(BaseRequester):
    def get_users(self):
        url = f"{self.base_url}/admin/users"
        with allure.step(f"GET {url} - запрос списка всех юзеров"):
            # отправка запроса на получение списка всех юзеров
            response = requests.get(url=url, headers=self.headers)
            allure.attach(
                response.text,
                "Ответ сервера",
                attachment_type=allure.attachment_type.JSON,
            )

        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)
        # т.к. сервер возвращает просто список словарей, без обёртки в объект,
        # то проще возвращать сырой ответ, чтобы потом отдельно каждый словарь валидировать с помощью модели Pydanitc
        return response.json()
