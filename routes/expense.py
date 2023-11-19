
from config.db import user_collection, group_collection, expense_collection, owes_collection

from fastapi import FastAPI, HTTPException
from bson import ObjectId
from fastapi import APIRouter
from models.models import User, Group, Expense, Owes, OwesResponse
from typing import List


expense_app = APIRouter()


@expense_app.post("/users/", response_model=User)
async def create_user(user: User):
    user_data = user.dict()
    inserted_user = user_collection.insert_one(user_data)
    user_id = str(inserted_user.inserted_id)
    return {**user_data, "id": user_id}


@expense_app.get("/users/{user_id}", response_model=User)
async def get_user_by_id(user_id: str):
    user = user_collection.find_one({"_id": ObjectId(user_id)})
    if user:
        return {**user, "id": str(user["_id"])}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@expense_app.get("/users/by_phone/{phone}", response_model=User)
async def get_user_by_phone(phone: str):
    user = user_collection.find_one({"phone": str(phone)})
    if user:
        return {**user, "id": str(user["phone"])}
    else:
        raise HTTPException(status_code=404, detail="User not found")


@expense_app.post("/groups/", response_model=Group)
async def create_group(group: Group):
    participants_exist = all(user_collection.find_one({"_id": ObjectId(user_id)}) for user_id in group.participants)
    if not participants_exist or not group.participants:
        raise HTTPException(status_code=400, detail="Invalid participants")

    group_data = group.dict()
    inserted_group = group_collection.insert_one(group_data)
    group_id = str(inserted_group.inserted_id)
    return {**group_data, "id": group_id}


# @expense_app.get("/groups/{group_id}", response_model=Group)
# async def get_group_by_id(group_id: str):
#     group = group_collection.find_one({"_id": ObjectId(group_id)})
#     if group:
#         return {**group, "id": str(group["_id"])}
#     else:
#         raise HTTPException(status_code=404, detail="Group not found")


@expense_app.get("/groups/{group_id}", response_model=Group)
async def get_group_by_id(group_id: str):
    group = group_collection.find_one({"_id": ObjectId(group_id)})
    if group:
        participant_names = []
        for participant_id in group["participants"]:
            participant = user_collection.find_one({"_id": ObjectId(participant_id)})
            if participant:
                participant_names.append(participant["name"])

        return {"participants": participant_names, "id": str(group["_id"])}
    else:
        raise HTTPException(status_code=404, detail="Group not found")


@expense_app.post("/expenses/", response_model=Expense)
async def create_expense(expense: Expense):
    group = group_collection.find_one({"_id": ObjectId(expense.group_id)})
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")

    participants = group["participants"]
    amount_per_person = expense.amount / len(participants)

    # Update the owes collection
    for participant in participants:
        if participant != expense.user_id:
            owes_data = {
                "payer": participant,
                "payee": expense.user_id,
                "amount": amount_per_person,
            }
            owes_collection.insert_one(owes_data)

    expense_data = expense.dict()
    inserted_expense = expense_collection.insert_one(expense_data)
    expense_id = str(inserted_expense.inserted_id)
    return {**expense_data, "id": expense_id}


@expense_app.get("/expenses/{expense_id}", response_model=Expense)
async def get_expense_by_id(expense_id: str):
    expense = expense_collection.find_one({"_id": ObjectId(expense_id)})
    if expense:
        return {**expense, "id": str(expense["_id"])}
    else:
        raise HTTPException(status_code=404, detail="Expense not found")


@expense_app.get("/owes/{user_id}", response_model=List[OwesResponse])
async def get_owes_for_user(user_id: str):
    # Get the list of owes for the given user_id
    owes = list(owes_collection.find({"payee": user_id}))

    # Fetch the names of the payer and payee from user_collection
    owes_response = []
    for owe in owes:
        payer = user_collection.find_one({"_id": ObjectId(owe["payer"])})
        payee = user_collection.find_one({"_id": ObjectId(owe["payee"])})

        if payer and payee:
            description = f"{payer['name']} owes {payee['name']} {owe['amount']}"
            owes_response.append({"description": description})

    return owes_response


@expense_app.get("/balances/{user_id}", response_model=List[OwesResponse])
async def get_balances_for_user(user_id: str):
    # Get the list of owes for the given user_id (both payer and payee)
    owes = list(owes_collection.find({"$or": [{"payer": user_id}, {"payee": user_id}]}))

    # Fetch the names of the payer and payee from user_collection
    balances_response = []
    for owe in owes:
        payer = user_collection.find_one({"_id": ObjectId(owe["payer"])})
        payee = user_collection.find_one({"_id": ObjectId(owe["payee"])})

        if payer and payee:
            description = f"{payer['name']} owes {payee['name']} {owe['amount']}"
            balances_response.append({"description": description})

    return balances_response