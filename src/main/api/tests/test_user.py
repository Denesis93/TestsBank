import pytest
from main.api.models.admin_login_request import AdminLoginRequestModel
from main.api.models.create_user_request import CreateUserRequestModel
from main.api.models.get_users_model_response import ResponseGetUsersModel
from main.api.models.login_user_request import LoginUserRequestModel
from main.api.requesters.create_user_requester import CreateUserPostBaseRequester
from main.api.requesters.delete_all_users_requester import DeleteAllUsersRequester
from main.api.requesters.delete_one_user_requester import DeleteOneUserRequester
from main.api.requesters.get_users_requester import GetUsersRequester
from main.api.requesters.login_user_requester import LoginUserPostBaseRequester
from main.api.specs.request_specs import RequestSpecs
from main.api.specs.response_specs import ResponseSpecs

"""Тесты для проверки сценариев, связанных с юзером"""


@pytest.mark.api
class TestUser:
    """Тест создания юзера с валидными данными"""

    def test_create_user_new(self, user_data, request_spec_admin, payload_create_user):

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_create_user)

        assert response_create_user.username == user_data["username"]
        assert response_create_user.role == user_data["role"]
        assert response_create_user.id > 0

    """Тест создания юзера с невалидными данными"""

    @pytest.mark.parametrize(
        "username, password",
        [
            ("Дэн", "Pas!sw0rd"),
            ("Denhkkhy89uljugyuggiuhgiu", "Pas!sw0rd"),
            ("Den!", "Pas!sw0rd"),
            ("Den", "пароль"),
        ],
    )
    def test_create_invalid_data(
        self, user_data, request_spec_admin, username, password
    ):

        # тело запроса на создание юзера с невалидными данными
        payload_create_user = CreateUserRequestModel(
            username=username, password=password, role="ROLE_USER"
        )

        # отправка запроса на создание юзера
        response_create_user = CreateUserPostBaseRequester(
            request_spec=request_spec_admin,
            response_spec=ResponseSpecs.bad_request_status(),
        ).post(payload_create_user)

        assert "error" in response_create_user

    """Тест логина под админом"""

    def test_admin_login(self):
        payload_login_admin = AdminLoginRequestModel(
            username="admin", password="123456"
        )

        response = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_login_admin)
        assert response.user.username == payload_login_admin.username
        assert response.user.role == "ROLE_ADMIN"

    """Тест логина под юзером с валидными данными"""

    def test_user_login(self, user_data, create_user):
        # тело запроса на логин юзера
        payload_user_login = LoginUserRequestModel(
            username=user_data["username"], password=user_data["password"]
        )

        # отправка запроса на логин юзера
        response_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.ok_status(),
        ).post(payload_user_login)

        assert response_user_login.user.username == user_data["username"]
        assert response_user_login.user.role == user_data["role"]
        assert response_user_login.token

    """Тест логина юзера с неправильным паролем"""

    def test_invalid_login(self, user_data, create_user):
        # тело запроса на логин юзера
        payload_user_login = LoginUserRequestModel(
            username=user_data["username"], password="Pas!sw0rdD"
        )

        # отправка запроса на логин юзера
        response_user_login = LoginUserPostBaseRequester(
            request_spec=RequestSpecs.unauth_request_spec(),
            response_spec=ResponseSpecs.unauthorized_status(),
        ).post(payload_user_login)

        assert response_user_login["error"] == "Invalid credentials"

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

    """Тест проверки удаления всех пользователей"""

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
