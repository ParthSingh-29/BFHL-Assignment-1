from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Account as AccountModel
from app.schemas import Account as AccountSchema

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_account(account: AccountSchema, db: Session = Depends(get_db)):
    db_account = AccountModel(**account.dict())
    db.add(db_account)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Account added successfully"}

@router.get("/{account_id}")
def get_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.AccountId == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@router.put("/{account_id}")
def update_account(account_id: str, account: AccountSchema, db: Session = Depends(get_db)):
    db_account = db.query(AccountModel).filter(AccountModel.AccountId == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    for key, value in account.dict().items():
        setattr(db_account, key, value)

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Account updated successfully"}

@router.delete("/{account_id}")
def delete_account(account_id: str, db: Session = Depends(get_db)):
    account = db.query(AccountModel).filter(AccountModel.AccountId == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    
    db.delete(account)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Account deleted successfully"}