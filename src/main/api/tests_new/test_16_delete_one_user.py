import pytest
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.models.get_users_model_response import ResponseGetUsersModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.delete_all_users_requester import DeleteAllUsersRequester
from main.api.requesters.delete_one_user_requester import DeleteOneUserRequester
from main.api.requesters.get_users_requester import GetUsersRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тесты на удаление одного пользователя"""


@pytest.mark.api
class TestDeleteOneUser:
    """Тест удаления одного юзера с валидными данными"""

    def test_delete_one_user(self, user_data, request_spec_admin):

        # в данном тесте не использую фикстуру на создание пользователя, т.к. в начале теста отправляю запрос на удаление всех пользователей
        # (следовательно, удаляется и созданный фикстурой пользователь)

        # запрос на удаление всех пользователей, чтобы очистить БД перед тестом (удалить всех ранее созданных в других тестах пользователей)
        DeleteAllUsersRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).delete_all()

        # тело запроса на создание юзера
        payload_create_user = CreateUserRequestModel(
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
        )

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_create_user)

        # получение айди юзера
        # user_id = response_create_user.id
        user_id = response_create_user.id

        # отправка запроса на удаление юзера
        response_one_user_delete = DeleteOneUserRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).delete_one(user_id=user_id)

        assert response_one_user_delete.message == "User deleted successfully"

        """Проверка, что юзер действительно был удалён из БД"""
        response_get_users = GetUsersRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).get_users()

        # т.к. возвращается список объектов юзеров без обёртки в объект,
        # то с помощью цикла валидирую каждый элемент списка в отдельности через Pydantic-модель
        users = [
            ResponseGetUsersModel.model_validate(user) for user in response_get_users
        ]
        assert (
            len(users) == 1
        )  # проверяю, что длина списка (количество объектов) равна одному объекту - админу
        assert users[0].username == "admin"
        assert users[0].role == "ROLE_ADMIN"


    """Тест удаления одного юзера с невалидными данными (удаление несуществующего юзера)"""

    def test_delete_one_user_invalid(self, user_data, request_spec_admin):

        # в данном тесте не использую фикстуру на создание пользователя, т.к. в начале теста отправляю запрос на удаление всех пользователей
        # (следовательно, удаляется и созданный фикстурой пользователь)

        # запрос на удаление всех пользователей, чтобы очистить БД перед тестом (удалить всех ранее созданных в других тестах пользователей)
        DeleteAllUsersRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).delete_all()

        # тело запроса на создание юзера, передающееся через модель
        payload_create_user = CreateUserRequestModel(
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
        )

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_create_user)

        # отправка запроса на удаление несуществующего юзера
        response_one_user_delete = DeleteOneUserRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.not_found_status(),
        ).delete_one(user_id=22)

        assert response_one_user_delete["error"] == "User not found"
