from src.main.api.models.base_model import BaseModel


class DepositResponseModel(BaseModel):
    id: int
    balance: float
