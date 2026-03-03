import json
from http import HTTPStatus
import allure
import requests
from main.api.models.transfer_request import TransferRequestModel
from main.api.models.transfer_response import TransferResponseModel
from main.api.requesters.post_base_requester import PostBaseRequester

"""Реквестер для перевода денежных средств"""


class TransferPostBaseRequester(PostBaseRequester):
    def post(self, transfer_request_model: TransferRequestModel):

        url = f"{self.base_url}/account/transfer"
        payload = transfer_request_model.model_dump(by_alias=True)
        with allure.step(f"POST {url} - перевод денежных средств"):
            allure.attach(
                json.dumps(payload, indent=4),
                "Тело запроса на перевод денежных средств",
                attachment_type=allure.attachment_type.JSON,
            )

            # отправка запроса на перевод денежных средств
            response = requests.post(
                url=url,
                headers=self.headers,
                json=payload,
            )
            allure.attach(
                response.text,
                "Тело ответа от сервера",
                attachment_type=allure.attachment_type.JSON,
            )
        with allure.step("Проверка статуса ответа"):
            self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            with allure.step("Валидация ответа сервера"):
                return TransferResponseModel.model_validate(response.json())
        return response.json()
