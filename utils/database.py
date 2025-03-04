from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from utils.config import DATABASE_URL
import os

load_dotenv()
Base = declarative_base()

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your environment variables.")

def init_db():
    from Address.models import Address
    from Users.models import User
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
