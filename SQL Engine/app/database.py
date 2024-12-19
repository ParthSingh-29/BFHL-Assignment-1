from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Replace with your MySQL connection details
DATABASE_URL = "mysql+mysqlconnector://root:1234@localhost/assignment1-updated"

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=True)

# Create a Session Local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for ORM models
Base = declarative_base()