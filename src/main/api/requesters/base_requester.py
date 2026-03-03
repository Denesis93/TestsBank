"""Базовый реквестер для методов ГЕТ и ДЕЛИТ, т.к. они используются редко и чтобы не плодить новые реквестеры из-за абстрактных методов"""


class BaseRequester:
    def __init__(self, request_spec, response_spec):
        self.headers = request_spec["headers"]
        self.base_url = request_spec["base_url"]
        self.response_spec = response_spec
