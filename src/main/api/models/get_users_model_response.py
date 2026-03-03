from main.api.models.base_model import BaseModel


class ResponseGetUsersModel(BaseModel):
    id: int
    username: str
    role: str
