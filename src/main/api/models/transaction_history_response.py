from src.main.api.models.base_model import BaseModel
from pydantic import Field
from datetime import datetime
from typing import Optional


class Transactions(BaseModel):
    transaction_id: int = Field(alias="transactionId")
    type: str
    amount: float
    from_account_id: Optional[int] = Field(
        alias="fromAccountId"
    )  # когда с сервера может возвращаться null
    to_account_id: int = Field(alias="toAccountId")
    created_at: datetime = Field(alias="createdAt")
    credit_id: Optional[int] = Field(
        alias="creditId"
    )  # когда с сервера может возвращаться null


class TransactionsHistoryResponseModel(BaseModel):
    id: int
    number: int
    balance: float
    transactions: list[Transactions]
