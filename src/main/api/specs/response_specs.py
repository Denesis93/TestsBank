from http import HTTPStatus
from requests import Response


class ResponseSpecs:
    @staticmethod
    # 200 код
    def ok_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text

        return confirm

    @staticmethod
    # 201 код
    def created_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.CREATED, response.text

        return confirm

    @staticmethod
    # 400 код
    def bad_request_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text

        return confirm

    @staticmethod
    # 404 код
    def not_found_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text

        return confirm

    @staticmethod
    # 401 код
    def unauthorized_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text

        return confirm

    @staticmethod
    # 403 код
    def forbidden_status():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text

        return confirm

    @staticmethod
    # 422 код
    def unprocessable_status():
        def confirm(response: Response):
            assert (
                response.status_code == HTTPStatus.UNPROCESSABLE_CONTENT
            ), response.text

        return confirm
