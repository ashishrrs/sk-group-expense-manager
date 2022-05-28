from routers import expensetracker
import uuid
from fastapi import HTTPException
import sys


def check(data: dict):

    for item in data["items"]:
        total_paid = 0
        total_owed = 0
        for payers in item["paid_by"]:
            for value in payers.values():
                total_paid += value
        for owers in item["owed_by"]:
            for value in owers.values():
                total_owed += value
        # print(total_paid)
        # print(total_owed)
        # print(item["value"])
        if item["value"] != total_paid or item["value"] != total_owed:
            return False
    return True


def add_group(data: dict):

    response = {}
    try:
        response["id"] = str(1)  # str(uuid.uuid1())
        response["name"] = data["name"]
        response["expenses"] = []
        response["members"] = data["members"]
        response["balances"] = {}
        response["group_expense"] = 0.0

        for member in data["members"]:
            response["balances"][member] = {}
            response["balances"][member]["total_balance"] = 0.0

        for member in data["members"]:
            flag = 0
            for user in expensetracker.users:
                if user["uname"] == member:
                    flag = 1
                    break

            if not flag:
                new_user = {}
                new_user["uname"] = member
                new_user["total_balance"] = 0.0
                expensetracker.users.append(new_user)

        expensetracker.groups.append(response)

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("add_group:", e, "at", str(exc_tb.tb_lineno))
        raise HTTPException(500)


async def add_expense(id: str, data: dict):

    try:
        flag = 0
        for group in expensetracker.groups:
            if group["id"] == id:
                flag = 1
                expense = {}
                expense["id"] = str(uuid.uuid1())
                expense["name"] = data["name"]
                expense["items"] = data["items"]
                assert check(data)
                for item in data["items"]:
                    group["group_expense"] += item["value"]
                    for payers in item["paid_by"]:
                        for member in payers.keys():
                            flag2 = 0
                            for user in expensetracker.users:
                                if user["uname"] == member:
                                    user["total_balance"] += payers[member]
                                    flag2 = 1
                                    break

                            if not flag2:
                                new_user = {}
                                new_user["uname"] = member
                                new_user["total_balance"] = payers[member]
                                expensetracker.users.append(new_user)

                            if member not in group["members"]:
                                group["members"].append(member)
                                group["balances"][member] = {}
                                group["balances"][member]["total_balance"] = 0.0
                            group["balances"][member]["total_balance"] += payers[member]

                    for owers in item["owed_by"]:
                        for member in owers.keys():
                            flag2 = 0
                            for user in expensetracker.users:
                                if user["uname"] == member:
                                    user["total_balance"] -= owers[member]
                                    flag2 = 1
                                    break

                            if not flag2:
                                new_user = {}
                                new_user["uname"] = member
                                new_user["total_balance"] = - \
                                    1*owers[member]
                                expensetracker.users.append(new_user)

                            if member not in group["members"]:
                                group["members"].append(member)
                                group["balances"][member] = {}
                                group["balances"][member]["total_balance"] = 0.0
                            group["balances"][member]["total_balance"] -= owers[member]
            expensetracker.expenses.append(expense)
            group["expenses"].append(expense["id"])
            break

        if not flag:
            raise HTTPException(500, "id does not exist")
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("add_expense:", e, "at", str(exc_tb.tb_lineno))
        raise HTTPException(500)


async def update_expense(group_id: str, id: str, data: dict):

    try:
        flag = 0
        for group in expensetracker.groups:
            if group["id"] == group_id:
                flag = 1
                flag2 = 0
                for expense in group["expenses"]:
                    if expense == id:
                        flag2 = 1
                        break
                if not flag2:
                    raise HTTPException(500, "no such expense exists")

                for expense in expensetracker.expenses:
                    if id == expense["id"]:
                        assert check(data)
                        expense["name"] = data["name"]
                        for item in expense["items"]:
                            group["group_expense"] -= item["value"]
                            for payers in item["paid_by"]:
                                for member in payers.keys():
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] -= payers[member]
                                            break
                                    group["balances"][member]["total_balance"] -= payers[member]

                            for owers in item["owed_by"]:
                                for member in owers.keys():
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] += owers[member]
                                            break
                                    group["balances"][member]["total_balance"] += owers[member]

                        for item in data["items"]:
                            group["group_expense"] += item["value"]
                            for payers in item["paid_by"]:
                                for member in payers.keys():
                                    flag2 = 0
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] += payers[member]
                                            flag2 = 1
                                            break

                                    if not flag2:
                                        new_user = {}
                                        new_user["uname"] = member
                                        new_user["total_balance"] = payers[member]
                                        expensetracker.users.append(new_user)

                                    if member not in group["members"]:
                                        group["members"].append(member)
                                        group["balances"][member] = {}
                                        group["balances"][member]["total_balance"] = 0.0
                                    group["balances"][member]["total_balance"] += payers[member]

                            for owers in item["owed_by"]:
                                for member in owers.keys():
                                    flag2 = 0
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] -= owers[member]
                                            flag2 = 1
                                            break

                                    if not flag2:
                                        new_user = {}
                                        new_user["uname"] = member
                                        new_user["total_balance"] = - \
                                            1*owers[member]
                                        expensetracker.users.append(new_user)

                                    if member not in group["members"]:
                                        group["members"].append(member)
                                        group["balances"][member] = {}
                                        group["balances"][member]["total_balance"] = 0.0
                                    group["balances"][member]["total_balance"] -= owers[member]
                        expense["items"] = data["items"]
                        break
                break

        if not flag:
            raise HTTPException(500, "id does not exist")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("add_expense:", e, "at", str(exc_tb.tb_lineno))
        raise HTTPException(500)


async def delete_expense(group_id: str, id: str):

    try:
        flag = 0
        for group in expensetracker.groups:
            if group["id"] == group_id:
                flag = 1
                flag2 = 0
                for expense in group["expenses"]:
                    if expense == id:
                        flag2 = 1
                        break
                if not flag2:
                    raise HTTPException(500, "no such expense exists")

                for i in range(len(expensetracker.expenses)):
                    if id == expensetracker.expenses[i]["id"]:
                        for item in expensetracker.expenses[i]["items"]:
                            group["group_expense"] -= item["value"]
                            for payers in item["paid_by"]:
                                for member in payers.keys():
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] -= payers[member]
                                            break
                                    group["balances"][member]["total_balance"] -= payers[member]

                            for owers in item["owed_by"]:
                                for member in owers.keys():
                                    for user in expensetracker.users:
                                        if user["uname"] == member:
                                            user["total_balance"] += owers[member]
                                            break
                                    group["balances"][member]["total_balance"] += owers[member]
                        del expensetracker.expenses[i]
                        break
                for i in range(len(group["expenses"])):
                    if group["expenses"][i] == id:
                        del group["expenses"][i]
                        break
                break

        if not flag:
            raise HTTPException(500, "id does not exist")

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        print("delete_expense:", e, "at", str(exc_tb.tb_lineno))
        raise HTTPException(500)
