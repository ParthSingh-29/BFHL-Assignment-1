from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import accounts, policies, claims

# Initialize the database
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Routers
app.include_router(accounts.router, prefix="/accounts", tags=["Accounts"])
app.include_router(claims.router, prefix="/claims", tags=["claims"])
app.include_router(policies.router, prefix="/policies", tags=["Policies"])

@app.get("/")
def root():
    return {"message": "BFHL Assignment 1"}

