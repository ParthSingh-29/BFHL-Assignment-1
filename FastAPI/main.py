#import libraries
from fastapi import FastAPI
from crud_operations import fetch_customer_info, add_account, add_policy, add_claim, delete_claim, delete_policy, delete_account, update_claim, update_policy, update_account
from models import Account, Policy, Claim


#create app
app= FastAPI()

#routes

@app.get("/")
async def load_root():
    return {"message":"BFHL Assignment 1"}

@app.get("/customers/{account_id}")
async def display_customer_info(account_id: str):
    return fetch_customer_info(account_id)

@app.post("/add_account/")
async def add_new_account(account: Account):
    return add_account(account)

@app.post("/add_policy/")
async def add_new_policy(policy: Policy):
    return add_policy(policy)

@app.post("/add_claim/")
async def add_new_claim(claim: Claim):
    return add_claim(claim)

@app.delete("/delete_claim/{claim_id}")
async def remove_claim(claim_id: str):
    return delete_claim(claim_id) 

@app.delete("/delete_policy/{han}")
async def remove_policy(han: str):
    return delete_policy(han)

@app.delete("/delete_account/{account_id}")
async def remove_account(account_id : str):
    return delete_account(account_id)

@app.put("/update_claim/{claim_id}")
async def update_claim_value(claim_id:str, updated_claim: Claim):
    return update_claim(claim_id, updated_claim)

@app.put("/update_policy/{han}")
async def update_policy_value(han:str, updated_policy: Policy):
    return update_policy(han, updated_policy)

@app.put("/update_account/{account_id}")
async def update_account_value(account_id:str, updated_account: Account):
    return update_account(account_id, updated_account)