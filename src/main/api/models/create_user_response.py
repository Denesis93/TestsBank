from src.main.api.models.base_model import BaseModel


class CreateUserResponseModel(BaseModel):
    id: int
    username: str
    password: str
    role: str
