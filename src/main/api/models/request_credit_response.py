from src.main.api.models.base_model import BaseModel
from pydantic import Field


class RequestCreditResponseModel(BaseModel):
    # account_id: int = Field(alias='accountId')  #на самом деле здесь приходит id, а не accountId. В сваггере ошибка
    id: int
    amount: float
    term_months: int = Field(alias="termMonths")
    balance: float
    credit_id: int = Field(alias="creditId")
