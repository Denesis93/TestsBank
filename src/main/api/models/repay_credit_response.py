from src.main.api.models.base_model import BaseModel
from pydantic import Field


class RepayCreditResponseModel(BaseModel):
    creditId: int
    amount_deposited: float = Field(alias="amountDeposited")
