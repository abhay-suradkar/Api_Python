from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.users import User 
from models.users import User
from models.users import User

def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Fetch user details by email from the Users table."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return user.email  # ✅ Return the email if found
