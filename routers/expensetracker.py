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


# Api to get all groups
@router.get("/groups/all", response_model=List[schemas.Group])
async def all_groups():
    return groups


# Api to get all expenses
@router.get("/expenses/all", response_model=List[schemas.Expense])
async def all_expenses():
    return expenses


# Api to get all users(for users i am considering username as unique)
@router.get("/users/all", response_model=List[schemas.User])
async def all_users():
    return users


@router.post("/groups/add")  # Api call to add new group
async def add_group(data: dict):
    utils.add_group(data)


# Api call to add new expense in a group
@router.post("/groups/{group_id}/add-expense")
async def add_expense(group_id: str, data: dict):
    await utils.add_expense(group_id, data)


# Api call to update expense in a group
@router.put("/groups/{group_id}/{id}/update-expense")
async def update_expense(group_id: str, id: str, data: dict):
    await utils.update_expense(group_id, id, data)


# Api call to delete expense in a group
@router.delete("/groups/{group_id}/{id}/delete-expense")
async def delete_expense(id: str, group_id: str):
    await utils.delete_expense(group_id, id)


# Api call to get group_balance
@router.get("/groups/{group_id}/group-expense", response_model=schemas.GroupExpense)
async def group_expense(group_id: str):
    try:
        flag = 0
        response = {}
        for group in groups:
            if group["id"] == group_id:
                flag = 1
                templist = []
                response["name"] = group["name"]
                response["balances"] = {}

                cnt = 0
                for i in range(len(group["members"])):
                    if group["balances"][group["members"][i]]["total_balance"] != 0:
                        templist.append(
                            (group["members"][i], group["balances"][group["members"][i]]["total_balance"]))
                        cnt += group["balances"][group["members"]
                                                 [i]]["total_balance"]
                    response["balances"][group["members"][i]] = {}
                    response["balances"][group["members"][i]
                                         ]["total_balance"] = group["balances"][group["members"][i]]["total_balance"]
                    response["balances"][group["members"][i]]["owes_to"] = []
                    response["balances"][group["members"][i]]["owed_by"] = []

                assert cnt == 0
                sortedlist = sorted(templist, key=lambda x: x[1])
                i = 0
                j = len(sortedlist)-1
                while i < j:

                    if abs(sortedlist[i][1]) < sortedlist[j][1]:
                        temp = {}
                        temp1 = {}
                        temp[sortedlist[i][0]] = abs(sortedlist[i][1])
                        temp1[sortedlist[j][0]] = abs(sortedlist[i][1])
                        response["balances"][sortedlist[i]
                                             [0]]["owes_to"].append(temp1)
                        response["balances"][sortedlist[j]
                                             [0]]["owed_by"].append(temp)
                        i += 1
                    elif abs(sortedlist[i][1]) > sortedlist[j][1]:
                        temp = {}
                        temp1 = {}
                        temp[sortedlist[i][0]] = sortedlist[j][1]
                        temp1[sortedlist[j][0]] = sortedlist[j][1]
                        response["balances"][sortedlist[i]
                                             [0]]["owes_to"].append(temp1)
                        response["balances"][sortedlist[j]
                                             [0]]["owed_by"].append(temp)
                        j -= 1
                    else:
                        temp = {}
                        temp1 = {}
                        temp[sortedlist[i][0]] = sortedlist[j][1]
                        temp1[sortedlist[j][0]] = sortedlist[j][1]
                        response["balances"][sortedlist[i]
                                             [0]]["owes_to"].append(temp1)
                        response["balances"][sortedlist[j]
                                             [0]]["owed_by"].append(temp)
                        i += 1
                        j -= 1

                return response
        if not flag:
            raise HTTPException(500, "id does not exist")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("group_expense:", e, "at", str(exc_tb.tb_lineno))
        raise HTTPException(500)
