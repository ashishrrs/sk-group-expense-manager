![alt text](https://github.com/ashishrrs/sk-group-expense-manager/blob/main/media/logo.png)
# *Splitkaro* 
# Group-Expense-Tracker
● Split Grocery and Food Bills from your Order History in 5 seconds.

● Fairest way to Split Bills.

● Pay-per-use by item wise splitting.

## Tech Stack : FastAPI
## Instrucions to setup and test

Run Group-Expense-Tracker APIs with following commands

```bash
    git clone https://github.com/ashishrrs/sk-group-expense-manager.git
    cd sk-group-expense-manager
    pip install -r requirements.txt
    uvicorn main:app --reload
```
Now got to http://127.0.0.1:8000/docs to run and test APIs using swagger UI.
## API Reference

#### Get all groups

```http
  GET /groups/all
```

#### Get all expenses

```http
  GET /expenses/all
```


#### Get all users

```http
  GET /users/all
```

#### Add new group

```http
  POST /groups/add
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `data` | `dict` | **Required**. Data dictionary having name and members as keys |

#### Add new expense

```http
  POST /groups/{group_id}/add-expense
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `group_id` | `str`| **Required**. Id of the group you want to add expense in |
| `data` | `dict` | **Required**. Data dictionary having name and items as keys |

#### Update expense
```http
  PUT /groups/{group_id}/{id}/update-expense
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `group_id` | `str`| **Required**. Id of the group you want to update expense from |
|`id`|`str`|**Required**. Id of the expense you want to update|
| `data` | `dict` | **Required**. Data dictionary having name and items as keys |


#### Delete expense
```http
  DELETE /groups/{group_id}/{id}/delete-expense
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `group_id` | `str`| **Required**. Id of the group you want to delete expense from |
|`id`|`str`|**Required**. Id of the expense you want to delete|


#### Get Group_Balance

```http
  GET /groups/{group_id}/group-expense
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `group_id` | `str`| **Required**. Id of the group you want to get group_balance of |
