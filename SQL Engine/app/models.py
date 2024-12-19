from sqlalchemy import Column, String, Integer, Float
from app.database import Base

# Account Table


class Account(Base):
    __tablename__ = "Accounts"

    AccountId = Column(String, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Age = Column(Integer, nullable=False)
    City = Column(String, nullable=False)
    State = Column(String, nullable=False)
    Pincode = Column(String, nullable=False)
    PolicyHan = Column(String, nullable=True)

# Policy Table


class Policy(Base):
    __tablename__ = "Policies"

    HAN = Column(String, primary_key=True, index=True)
    PolicyName = Column(String, nullable=False)
    AccountId = Column(String, nullable=False)

# Claim Table


class Claim(Base):
    __tablename__ = "Claims"

    Id = Column(String, primary_key=True, index=True)
    CreatedDate = Column(String, nullable=False)
    CaseNumber = Column(String, nullable=False)
    HAN = Column(String, nullable=False)
    BillAmount = Column(Float, nullable=False)
    AccountId = Column(String, nullable=False)
    Status = Column(String, nullable=False)
