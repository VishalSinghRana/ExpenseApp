from pydantic import BaseModel
from typing import List


class User(BaseModel):
    name: str
    email: str
    phone: str


class Group(BaseModel):
    participants: List[str]


class Expense(BaseModel):
    transaction_name: str
    transaction_type: str
    group_id: str
    user_id: str
    amount: float


class Owes(BaseModel):
    payer: str
    payee: str
    amount: float


class OwesResponse(BaseModel):
    description: str

