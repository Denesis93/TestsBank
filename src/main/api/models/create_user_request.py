from src.main.api.models.base_model import BaseModel


class CreateUserRequestModel(BaseModel):
    username: str
    password: str
    role: str
