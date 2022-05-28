from typing import List, Optional
from pydantic import BaseModel


class Group(BaseModel):
    id: str
    name: str
    expenses: List[str]
    members: List[str]
    balances: dict
    group_expense: float


class Expense(BaseModel):
    id: str
    name: str
    items: List[dict]


class User(BaseModel):
    uname: str
    total_balance: float


class GroupExpense(BaseModel):
    name: str
    balances: dict
