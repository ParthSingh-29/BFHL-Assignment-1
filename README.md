# BFHL-Assignment-1

## Data Preprocessing:

1. Replaced the missing values with 'None'
   
2. Primary key for each individual table:

    Account -> AccountId
   
    Policy -> HAN
   
    Claim -> Id
  
4. Created the mapping of accounts to policies, and polices to claims
   i. For accounts to policy: One account can have more than one policy, two accounts can not have one policy
   ii. For policy to claims: One policy can have multiple claims

5. Extra columns created: PolicyHAN in Accounts, AccountId in Polices


## FastAPI

  Functionalities:
  1. Fetch Customer Information
  2. Add Account
  3. Add Policy
  4. Add Claim
  5. Delete Claim
  6. Delete Policy
  7. Delete Account
  8. Update Claim
  9. Update Policy
  10. Update Account

  All these functionalites are updated directly in the excel files along with logs.

## SQl Engine:

  Functionalites: 

  1. Fetch Customer Information
  2. Add Account
  3. Add Policy
  4. Add Claim
  5. Delete Claim
  6. Delete Policy
  7. Delete Account
  8. Update Claim
  9. Update Policy
  10. Update Account
