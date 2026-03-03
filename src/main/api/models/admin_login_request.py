from src.main.api.models.base_model import BaseModel


class AdminLoginRequestModel(BaseModel):
    username: str
    password: str
