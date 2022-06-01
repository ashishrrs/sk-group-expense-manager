from routers import expensetracker
import uuid
import asyncio
from fastapi import HTTPException
import sys


def check(data: dict):  # check fucntion to check that paid money == total owed money == value of item

    for item in data["items"]:
        total_paid = 0
        total_owed = 0
        for payers in item["paid_by"]:
            for value in payers.values():
                total_paid += value
        for owers in item["owed_by"]:
            for value in owers.values():
                total_owed += value
        if item["value"] != total_paid or item["value"] != total_owed:
            return False
    return True


async def add_group(data: dict):  # function to add groups

    response = {}
    try:
        response["id"] = str(uuid.uuid1())
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


async def add_expense(group_id: str, data: dict):  # fucntion to add expenses

    try:
        flag = 0
        # await asyncio.sleep(10)
        for group in expensetracker.groups:
            if group["id"] == group_id:
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


# fucntion to update expenses
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


async def delete_expense(group_id: str, id: str):  # fucntion to delete expense

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


async def group_expense(group_id: str):  # fucntion to delete expense
    try:
        flag = 0
        response = {}
        for group in expensetracker.groups:
            if group["id"] == group_id:
                flag = 1
                pos_val_list = []
                neg_val_list = []
                response["name"] = group["name"]
                response["balances"] = {}

                cnt = 0
                for i in range(len(group["members"])):
                    if group["balances"][group["members"][i]]["total_balance"] != 0:
                        if group["balances"][group["members"][i]]["total_balance"] > 0:
                            pos_val_list.append((group["members"][i], group["balances"][group["members"][i]]["total_balance"]))
                        else:
                            neg_val_list.append((group["members"][i], group["balances"][group["members"][i]]["total_balance"]))
                        cnt += group["balances"][group["members"]
                                                 [i]]["total_balance"]
                    response["balances"][group["members"][i]] = {}
                    response["balances"][group["members"][i]
                                         ]["total_balance"] = group["balances"][group["members"][i]]["total_balance"]
                    response["balances"][group["members"][i]]["owes_to"] = []
                    response["balances"][group["members"][i]]["owed_by"] = []

                assert cnt == 0
                templist = []
                for i in range(len(pos_val_list)):
                    flag1 = 0
                    for j in range(len(neg_val_list)):
                        if abs(neg_val_list[j][1]) == pos_val_list[i][1]:
                            flag1 = 1
                            temp = {}
                            temp1 = {}
                            temp[neg_val_list[j][0]] = pos_val_list[i][1]
                            temp1[pos_val_list[i][0]] = pos_val_list[i][1]
                            response["balances"][neg_val_list[j][0]]["owes_to"].append(temp1)
                            response["balances"][pos_val_list[i][0]]["owed_by"].append(temp)
                            del neg_val_list[j]
                            break
                    if not flag1:
                        templist.append(pos_val_list[i])


                for i in range(len(neg_val_list)):
                    templist.append(neg_val_list[i])




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
