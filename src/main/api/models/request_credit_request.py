from src.main.api.models.base_model import BaseModel
from pydantic import Field


class RequestCreditRequestModel(BaseModel):
    account_id: int = Field(alias="accountId")
    amount: float
    term_months: int = Field(alias="termMonths")
