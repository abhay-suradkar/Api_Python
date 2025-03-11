from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from utils.config import DATABASE_URL
import os

# Load .env variables (optional if you're using a config file)
load_dotenv()

# Validate DATABASE_URL before doing anything
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your environment variables or config file.")

# Create Base only once
Base = declarative_base()

# Use the validated DATABASE_URL
SQLALCHEMY_DATABASE_URL = DATABASE_URL

# Create SQLAlchemy engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Initialize DB and create tables
def init_db():
    from Address.models import Address
    from Users.models import User
    Base.metadata.create_all(bind=engine)

# Dependency for getting DB session (used in FastAPI routes)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
