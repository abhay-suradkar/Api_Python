from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from schemas.user import UserSignup, UserLogin, ResetPassword
from auth_utils import hash_password, verify_password

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup/")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = hash_password(user.password)

    new_user = User(name=user.name, email=user.email, mobile=user.mobile, password=hashed_password)
    
    db.add(new_user)
    db.commit()
     
    return {"message": "User registered successfully"}

@router.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if not existing_user or not verify_password(user.password, existing_user.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": "Login successful"}

@router.get("/get")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    users_data = [{"email": user.email, "name": user.name, "mobile": user.mobile} for user in users]
    return {"total_users": len(users), "users": users_data}

@router.put("/reset-password/")
def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.new_password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    hashed_password = hash_password(data.new_password)
    user.password = hashed_password
    db.commit()

    return {"message": "Password updated successfully"}

@router.delete("/delete-user/{email}")
def delete_user(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}
