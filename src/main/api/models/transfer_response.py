from src.main.api.models.base_model import BaseModel
from pydantic import Field


class TransferResponseModel(BaseModel):
    to_account_id: int = Field(alias="toAccountId")
    from_account_id: int = Field(alias="fromAccountId")
    from_account_id_balance: float = Field(alias="fromAccountIdBalance")
