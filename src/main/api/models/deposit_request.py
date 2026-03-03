from src.main.api.models.base_model import BaseModel
from pydantic import Field


class DepositRequestModel(BaseModel):
    account_id: int = Field(
        alias="accountId"
    )  # перевожу в питонячий snake_case, но по сваггеру должно называться accountId(в JSON)
    amount: float
