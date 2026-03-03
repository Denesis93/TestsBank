from main.api.models.base_model import BaseModel


class DeleteAllUsersResponseModel(BaseModel):
    message: str
    deleted_count: int
