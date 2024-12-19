from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.models import Policy
from app.database import SessionLocal
from app.models import Policy as PolicyModel
from app.schemas import Claim as PolicySchema
from datetime import datetime

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=dict)
def create_policy(policy: PolicySchema, db: Session = get_db()):
    new_policy = PolicyModel(**policy.dict())
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)

    return {"message": "Policy created successfully", "policy": new_policy}


@router.put("/{policy_id}", response_model=dict)
def update_policy(policy_id: int, policy: PolicySchema, db: Session = get_db()):
    existing_policy = db.query(PolicyModel).filter(PolicyModel.id == policy_id).first()
    if not existing_policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    for key, value in policy.dict(exclude_unset=True).items():
        setattr(existing_policy, key, value)

    db.commit()
    db.refresh(existing_policy)

    return {"message": "Policy updated successfully", "policy": existing_policy}


@router.delete("/{policy_id}", response_model=dict)
def delete_policy(policy_id: int, db: Session = get_db()):
    existing_policy = db.query(PolicyModel).filter(PolicyModel.id == policy_id).first()
    if not existing_policy:
        raise HTTPException(status_code=404, detail="Policy not found")

    db.delete(existing_policy)
    db.commit()

    return {"message": "Policy deleted successfully"}
