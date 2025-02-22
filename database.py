from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()

host = "api-abhaysuradkar8-a890.h.aivencloud.com"
port = 14565
username = "avnadmin"
password = "AVNS_LvAKQwNqoVR1Zq_4YL1"
database = "defaultdb"
# schema = "public"

DATABASE_URL = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# DATABASE_URL = os.getenv("DATABASE_URL")
# DATABASE_URL = "postgresql://avnadmin:AVNS_LvAKQwNqoVR1Zq_4YL1@api-abhaysuradkar8-a890.h.aivencloud.com:14565/defaultdb"

SQLALCHEMY_DATABASE_URL = DATABASE_URL

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a SessionLocal class to handle database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Check your environment variables.")

# engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    from models.address import Address
    from models.user import User
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
