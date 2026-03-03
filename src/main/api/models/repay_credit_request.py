from src.main.api.models.base_model import BaseModel
from pydantic import Field


class RepayCreditRequestModel(BaseModel):
    credit_id: int = Field(alias="creditId")
    account_id: int = Field(alias="accountId")
    amount: float
