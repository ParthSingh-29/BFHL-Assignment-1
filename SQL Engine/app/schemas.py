from pydantic import BaseModel

class Account(BaseModel):
    AccountId: str
    Name: str
    Age: int
    City: str
    State: str
    Pincode: str
    PolicyHan: str | None

    class Config:
        orm_mode = True

class Policy(BaseModel):
    HAN: str
    PolicyName: str
    AccountId: str

    class Config:
        orm_mode = True

class Claim(BaseModel):
    Id: str
    CreatedDate: str
    CaseNumber: str
    HAN: str
    BillAmount: float
    AccountId: str
    Status: str

    class Config:
        orm_mode = True
