from src.main.api.models.base_model import BaseModel
from pydantic import Field


class TransferRequestModel(BaseModel):
    from_account_id: int = Field(alias="fromAccountId")
    to_account_id: int = Field(alias="toAccountId")
    amount: float
