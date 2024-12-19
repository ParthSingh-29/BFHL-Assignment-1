# import libraries
import pandas as pd
import random
import string
from fastapi import HTTPException
from models import Account, Policy, Claim
from datetime import datetime
from loguru import logger


# import dataframes
accounts_df = pd.read_excel(
    "Assignment1-Updated.xlsx", sheet_name="Accounts").replace({float("nan"): None})
claims_df = pd.read_excel("Assignment1-Updated.xlsx",
                          sheet_name="Claims").replace({float("nan"): None})
policies_df = pd.read_excel(
    "Assignment1-Updated.xlsx", sheet_name="Policies").replace({float("nan"): None})

# New log dataframe to store logs
log_df = pd.DataFrame(columns=["Timestamp", "Action", "Details"])

# Function to log actions


def log_action(action: str, details: str):
    global log_df
    timestamp = datetime.now()
    log_entry = pd.DataFrame({"Timestamp": [timestamp], "Action": [
                             action], "Details": [details]})
    log_df = pd.concat([log_df, log_entry], ignore_index=True)

    # Save the logs to an Excel sheet
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            log_df.to_excel(writer, sheet_name="Logs", index=False)
    except Exception as e:
        logger.error(f"Error saving log: {str(e)}")


# function to fetch customer info
def fetch_customer_info(account_id: str):

    # check if customer exists
    account = accounts_df[accounts_df["AccountId"] == account_id]
    if (account.empty):
        raise HTTPException(status_code=404, detail="Account does not exist.")

    # fetch policy info
    policies = []
    han_values = account["PolicyHan"].to_string(index=False).split(', ')
    for han in han_values:
        policy = policies_df[policies_df["HAN"] == han]
        policies.append(policy)
    policies = pd.concat(policies, ignore_index=True)

    # fetch claims info
    claims = claims_df[claims_df["AccountId"] == account_id]

    log_action("Fetch Customer Info", f"Fetched info for account {account_id}")

    # print output
    return ({
        "Accounts": account.to_dict(orient="records"),
        "Policies": policies.to_dict(orient="records"),
        "Claims": claims.to_dict(orient="records")
    })


# function to add account
def add_account(account: Account):

    # generate account id
    def generate_account_id():
        characters = string.ascii_uppercase + string.digits
        while True:
            new_id = ''.join(random.choices(characters, k=18))
            if new_id not in accounts_df["AccountId"].astype(str).to_list():
                return new_id
    account_id = generate_account_id()

    # add account to dataframe
    accounts_df.loc[len(accounts_df)] = {
        "AccountId": account_id,
        "Name": account.Name,
        "Age": account.Age,
        "City": account.City,
        "State": account.State,
        "Pincode": account.Pincode,
        "PolicyHan": None
    }

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            accounts_df.to_excel(writer, sheet_name="Accounts", index=False)

        log_action("Add Account", f"Account {account_id} added")

        return ({
            "message": "Account added",
            "Account ID": account_id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# function to add policy of existing user
def add_policy(policy: Policy):

    # check if account exists
    if policy.AccountId not in accounts_df["AccountId"].astype(str).to_list():
        raise HTTPException(status_code=400, detail="Account does not exist")

    # generate han
    def generate_han():
        characters = string.ascii_uppercase + string.digits
        while True:
            new_id = ''.join(random.choices(characters, k=18))
            if new_id not in policies_df["HAN"].astype(str).to_list():
                return new_id
    han = generate_han()

    # add policy to dataframe
    policies_df.loc[len(policies_df)] = {
        "HAN": han,
        "Policy Name": policy.PolicyName,
        "AccountId": policy.AccountId
    }

    # update the accounts dataframe
    accounts_df.loc[accounts_df['AccountId'] == policy.AccountId, 'PolicyHan'] = \
        accounts_df.loc[accounts_df['AccountId'] == policy.AccountId, 'PolicyHan'].apply(
        lambda x: (x + ', ' + han) if x else han
    )

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            accounts_df.to_excel(writer, sheet_name="Accounts", index=False)
            policies_df.to_excel(writer, sheet_name="Policies", index=False)

        log_action(
            "Add Policy", f"Policy {han} added to Account {policy.AccountId}")

        return ({
            "message": "Policy added",
            "HAN": han
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# function to add claim of existing user with policy
def add_claim(claim: Claim):

    # check if account exists or not
    if (claim.AccountId not in accounts_df["AccountId"].astype(str).to_list()):
        raise HTTPException(status_code=400, detail="Account does not exist")

    # check if policy exists or not
    if (claim.HAN not in policies_df["HAN"].astype(str).to_list()):
        raise HTTPException(status_code=400, detail="Policy does not exist")

    # generate id
    def generate_id():
        characters = string.ascii_uppercase + string.digits
        while True:
            new_id = ''.join(random.choices(characters, k=18))
            if new_id not in claims_df["Id"].astype(str).to_list():
                return new_id
    id = generate_id()

    # generate casenumber
    def generate_casenumber():
        characters = string.ascii_uppercase + string.digits
        while True:
            new_id = ''.join(random.choices(characters, k=18))
            if new_id not in claims_df["CaseNumber"].astype(str).to_list():
                return new_id
    casenumber = generate_casenumber()

    # add claim to dataframe
    claims_df.loc[len(claims_df)] = {
        "Id": id,
        "CreatedDate": datetime.now(),
        "CaseNumber": casenumber,
        "HAN": claim.HAN,
        "BillAmount": claim.BillAmount,
        "AccountId": claim.AccountId,
        "Status": claim.Status
    }

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            claims_df.to_excel(writer, sheet_name="Claims", index=False)

        log_action("Add Claim", f"Claim {id} added for Policy {claim.HAN}")

        return ({
            "message": "Claime added",
            "Claim ID": id
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")

# function to delete a claim


def delete_claim(claim_id: str):
    global claims_df
    # check if claim exists
    if claim_id not in claims_df["Id"].astype(str).to_list():
        raise HTTPException(status_code=404, detail="Claim does not exist")

    # remove claim from dataframe
    claims_df = claims_df[claims_df["Id"] != claim_id]

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            claims_df.to_excel(writer, sheet_name="Claims", index=False)

        log_action("Delete Claim", f"Claim {claim_id} deleted.")

        return ({
            "message": "Claim deleted"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# function to delete a policy and its claims
def delete_policy(han: str):
    global policies_df, claims_df
    # check if policy exists
    if han not in policies_df["HAN"].astype(str).to_list():
        raise HTTPException(status_code=400, detail="Policy does not exist")

    # remove the policy
    policies_df = policies_df[policies_df["HAN"] != han]

    # remove the claims of that policy
    claims_df = claims_df[claims_df["HAN"] != han]

    # remove the policy from the account
    account_index = accounts_df[accounts_df['PolicyHan'].apply(
        lambda x: han in x if isinstance(x, list) else False)].index
    if not account_index.empty:
        accounts_df.loc[account_index, 'PolicyHan'] = accounts_df.loc[account_index, 'PolicyHan'].apply(
            lambda x: [han for han in x if han != han]
        )

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            claims_df.to_excel(writer, sheet_name="Claims", index=False)
            policies_df.to_excel(writer, sheet_name="Policies", index=False)
            accounts_df.to_excel(writer, sheet_name="Accounts", index=False)

        log_action("Delete Policy", f"Policy {han} deleted.")

        return ({
            "message": "Policy deleted"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# function to delete account along with its policies and claims
def delete_account(account_id):
    global policies_df, claims_df, accounts_df

    # check if account exists
    if account_id not in accounts_df["AccountId"].astype(str).to_list():
        raise HTTPException(status_code=400, detail="Account does not exist")

    # remove the policy and its claims
    account = accounts_df[accounts_df["AccountId"] == account_id]
    han_values = account["PolicyHan"].to_string(index=False).split(', ')
    for han in han_values:
        delete_policy(han)

    # remove the account from dataframe
    accounts_df = accounts_df[accounts_df["AccountId"] != account_id]

    # write the dataframe into excel workbook
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", if_sheet_exists="replace", mode='a') as writer:
            accounts_df.to_excel(writer, sheet_name="Accounts", index=False)

        log_action("Delete Account",
                   f"Account {account_id} deleted along with associated policies and claims.")

        return ({
            "message": "Account deleted"
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# function to update the claim
def update_claim(claim_id: str, updated_claim: Claim):
    global claims_df

    # Check if the claim exists
    if claim_id not in claims_df["Id"].astype(str).values:
        raise HTTPException(status_code=404, detail="Claim not found")

    # Get the index of the claim to update
    claim_index = claims_df[claims_df["Id"].astype(str) == claim_id].index[0]

    # Convert the Pydantic model to a dictionary, excluding unset fields
    updates_dict = updated_claim.dict(exclude_unset=True)

    # Validate fields
    valid_fields = set(claims_df.columns) - {"Id", "HAN"}
    invalid_fields = [key for key in updates_dict if key not in valid_fields]
    if invalid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid fields in update: {invalid_fields}")

    # Apply the updates to the DataFrame
    for field, value in updates_dict.items():
        if field in valid_fields:
            claims_df.at[claim_index, field] = value

    # Save the updated DataFrame to the Excel file
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            claims_df.to_excel(writer, sheet_name="Claims", index=False)

        log_action("Update Claim", f"Claim {claim_id} updated.")

        return {"message": "Claim updated successfully", "updated_data": claims_df.iloc[claim_index].to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving Excel: {str(e)}")


# function to update policy
def update_policy(han: str, updated_policy: Policy):
    global policies_df

    # Check if the policy exists using HAN
    if han not in policies_df["HAN"].astype(str).values:
        raise HTTPException(status_code=404, detail="Policy not found")

    # Get the index of the policy to update
    policy_index = policies_df[policies_df["HAN"].astype(str) == han].index[0]

    # Convert the Pydantic model to a dictionary, excluding unset fields
    updates_dict = updated_policy.dict(exclude_unset=True)

    # Validate fields
    valid_fields = set(policies_df.columns) - {"HAN", "AccountId"}
    invalid_fields = [key for key in updates_dict if key not in valid_fields]
    if invalid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid fields in update: {invalid_fields}")

    # Apply the updates to the DataFrame
    for field, value in updates_dict.items():
        if field in valid_fields:
            policies_df.at[policy_index, field] = value

    # Save the updated DataFrame to the Excel file
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            policies_df.to_excel(writer, sheet_name="Policies", index=False)

        log_action("Update Policy", f"Policy {han} updated.")

        return {"message": "Policy updated successfully", "updated_data": policies_df.iloc[policy_index].to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving Excel: {str(e)}")


# function to update account
def update_account(account_id: str, updated_account: Account):
    global accounts_df

    # Check if the account exists using AccountId
    if account_id not in accounts_df["AccountId"].astype(str).values:
        raise HTTPException(status_code=404, detail="Account not found")

    # Get the index of the account to update
    account_index = accounts_df[accounts_df["AccountId"].astype(
        str) == account_id].index[0]

    # Convert the Pydantic model to a dictionary, excluding unset fields
    updates_dict = updated_account.dict(exclude_unset=True)

    # Validate fields
    # Only these fields can be updated
    valid_fields = set(["Name", "City", "State", "Pincode", "Age"])
    invalid_fields = [key for key in updates_dict if key not in valid_fields]
    if invalid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid fields in update: {invalid_fields}")

    # Apply the updates to the DataFrame
    for field, value in updates_dict.items():
        if field in valid_fields:
            accounts_df.at[account_index, field] = value

    # Save the updated DataFrame to the Excel file
    try:
        with pd.ExcelWriter("Assignment1-Updated.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
            accounts_df.to_excel(writer, sheet_name="Accounts", index=False)

        log_action("Update Account", f"Account {account_id} updated.")

        return {"message": "Account updated successfully", "updated_data": accounts_df.iloc[account_index].to_dict()}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error saving Excel: {str(e)}")
