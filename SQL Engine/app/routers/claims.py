from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session
from app.models import Claim
from app.database import SessionLocal
from app.models import Claim as ClaimModel
from app.schemas import Claim as ClaimSchema
from datetime import datetime

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_claim(claim: ClaimSchema, db: Session = get_db()):
    new_claim = ClaimModel(**claim.dict())
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)

    return {"message": "Claim created successfully", "claim": new_claim}

@router.put("/{claim_id}", response_model=dict)
def update_claim(claim_id: int, claim: ClaimSchema, db: Session = get_db()):
    existing_claim = db.query(ClaimModel).filter(ClaimModel.id == claim_id).first()
    if not existing_claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    for key, value in claim.dict(exclude_unset=True).items():
        setattr(existing_claim, key, value)

    db.commit()
    db.refresh(existing_claim)

    return {"message": "Claim updated successfully", "claim": existing_claim}

@router.delete("/{claim_id}", response_model=dict)
def delete_claim(claim_id: int, db: Session = get_db()):
    existing_claim = db.query(ClaimModel).filter(ClaimModel.id == claim_id).first()
    if not existing_claim:
        raise HTTPException(status_code=404, detail="Claim not found")

    db.delete(existing_claim)
    db.commit()

    return {"message": "Claim deleted successfully"}
