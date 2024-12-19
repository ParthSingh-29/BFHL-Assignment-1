from pydantic import BaseModel
from typing import Optional

class Account(BaseModel):
    Name: Optional[str]=None
    Age: Optional[int]=None
    City: Optional[str]=None
    State: Optional[str]=None
    Pincode: Optional[int]=None

class Policy(BaseModel):
    PolicyName: Optional[str]=None
    AccountId: Optional[str]=None

class Claim(BaseModel):
    HAN: Optional[str]=None
    BillAmount: Optional[int]=None
    Status: Optional[str]=None
    AccountId: Optional[str]=None