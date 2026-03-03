from src.main.api.models.base_model import BaseModel


class CreateAccountResponseModel(BaseModel):
    id: int
    number: str
    balance: float
