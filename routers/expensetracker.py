import uuid
import schemas
from typing import List, Optional
from fastapi import APIRouter, status, HTTPException
from repository import utils
import sys
import uuid
groups = []
expenses = []
users = []
router = APIRouter()
import asyncio

transaction_lock = asyncio.Lock()
# Api to get all groups
@router.get("/groups/all", response_model=List[schemas.Group])
def all_groups():
    return groups


# Api to get all expenses
@router.get("/expenses/all", response_model=List[schemas.Expense])
def all_expenses():
    return expenses


# Api to get all users(for users i am considering username as unique)
@router.get("/users/all", response_model=List[schemas.User])
def all_users():
    return users


@router.post("/groups/add")  # Api call to add new group
async def add_group(data: dict):
    await utils.add_group(data)


# Api call to add new expense in a group
@router.post("/groups/{group_id}/add-expense")
async def add_expense(group_id: str, data: dict):
    async with transaction_lock:
        await utils.add_expense(group_id, data)


# Api call to update expense in a group
@router.put("/groups/{group_id}/{id}/update-expense")
async def update_expense(group_id: str, id: str, data: dict):
    async with transaction_lock:
        await utils.update_expense(group_id, id, data)


# Api call to delete expense in a group
@router.delete("/groups/{group_id}/{id}/delete-expense")
async def delete_expense(id: str, group_id: str):
    async with transaction_lock:
        await utils.delete_expense(group_id, id)


# Api call to get group_balance
@router.get("/groups/{group_id}/group-expense", response_model=schemas.GroupExpense)
async def group_expense(group_id: str):
    async with transaction_lock:
        response = await utils.group_expense(group_id)
        return response