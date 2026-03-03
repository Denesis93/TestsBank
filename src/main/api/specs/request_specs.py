import requests
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.models.login_user_response import LoginUserResponseModel


class RequestSpecs:
    # Базовый адрес API — используется во всех запросах
    BASE_URL = "http://localhost:4111/api"

    @staticmethod
    def base_headers():
        """
        Возвращает базовые заголовки для любого запроса.
        Говорим серверу, что работаем с JSON.
        """
        return {
            "accept": "application/json",  # ожидаем ответ в формате JSON
            "Content-Type": "application/json",  # отправляем данные в формате JSON
        }

    @staticmethod
    def login_and_get_request_spec(username: str, password: str):
        """
        Логинится под пользователем и возвращает:
        - headers с токеном (Authorization)
        - base_url
        Используется для авторизованных запросов.
        """

        # Создаём модель с логином и паролем
        payload = LoginUserRequestModel(username=username, password=password)

        # Отправляем POST-запрос на эндпоинт логина
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",  # endpoint логина
            json=payload.model_dump(),  # преобразуем модель в dict
            headers=RequestSpecs.base_headers(),  # передаём базовые заголовки
        )

        # Проверяем, что логин прошёл успешно
        if response.status_code == 200:

            # Валидируем ответ через Pydantic-модель
            response_data = LoginUserResponseModel.model_validate(response.json())

            # Достаём токен из ответа
            token = response_data.token

            # Берём базовые заголовки
            headers = RequestSpecs.base_headers()

            # Добавляем токен в заголовки (авторизация)
            headers["Authorization"] = f"Bearer {token}"

            # Возвращаем словарь с готовыми данными для Requester
            return {
                "headers": headers,  # заголовки с токеном
                "base_url": RequestSpecs.BASE_URL,  # базовый URL
            }

        # Если логин не прошёл — сразу падаем
        raise Exception("Login was failed")

    @staticmethod
    def unauth_request_spec():
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": RequestSpecs.BASE_URL,
        }
