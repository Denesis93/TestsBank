from src.main.api.models.base_model import BaseModel


class LoginUserRequestModel(BaseModel):
    username: str
    password: str
