import pytest
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.models.get_users_model_response import ResponseGetUsersModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.delete_all_users_requester import DeleteAllUsersRequester
from main.api.requesters.get_users_requester import GetUsersRequester
from main.api.specs.response_specs import ResponseSpecs

"""Тест проверки удаления всех пользователей"""


@pytest.mark.api
class TestDeleteAllUsers:
    def test_delete_all_users(self, user_data, user_2_data, request_spec_admin):

        # в данном тесте не использую фикстуру на создание пользователя, т.к. в начале теста отправляю запрос на удаление всех пользователей
        # (следовательно, удаляются и созданные фикстурой пользователи)

        # выношу в переменную, как часто встречаю
        # запрос на удаление всех пользователей, чтобы очистить БД перед тестом (удалить всех ранее созданных пользователей в других тестах)
        DeleteAllUsersRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).delete_all()

        # тело для запроса на создание юзера 1
        payload_user_1_create = CreateUserRequestModel(
            username=user_data["username"],
            password=user_data["password"],
            role=user_data["role"],
        )

        # тело для запроса на создание юзера 2
        payload_user_2_create = CreateUserRequestModel(
            username=user_2_data["username"],
            password=user_2_data["password"],
            role=user_2_data["role"],
        )

        # отправка запроса на создание юзера №1
        CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_user_1_create)

        # отправка запроса на создание юзера №2
        CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_user_2_create)

        # запрос на удаление всех пользователей
        response_all_users_delete = DeleteAllUsersRequester(
            request_spec=request_spec_admin, response_spec=ResponseSpecs.ok_status()
        ).delete_all()

        assert (
            response_all_users_delete.message
            == "All users except current admin deleted successfully"
        )
        assert response_all_users_delete.deleted_count == 2

        """Проверка, что все пользователи действительно были удалены"""

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
