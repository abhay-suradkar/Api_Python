from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import SessionLocal, get_db
from Users.models import User
from Users.schemas import UserSignup, UserLogin, ResetPassword, DeleteUser
from auth_utils import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
import jwt
from jose import JWTError, jwt

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.CrdKYwmgazyXb2ZfxMsKLxkV44Lv9D4MQLUyaynuNdI"
ALGORITHM = "HS256"
class UserService:
  
    def signup_user(user: UserSignup, db: Session = Depends(get_db)):    
        try:
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
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def login(user: UserLogin, db: Session = Depends(get_db)):
        try:
            existing_user = db.query(User).filter(User.email == user.email).first()
            if not existing_user:
                raise HTTPException(status_code=400, detail="Invalid email")

            if not verify_password(user.password, existing_user.password):
                raise HTTPException(status_code=400, detail="Invalid password")

            access_token = create_access_token({"email": existing_user.email})
            refresh_token = create_refresh_token({"email": existing_user.email})
            return {
                    "Message":"Login Sucessfully",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "token_type": "Bearer"
                    }
  
        except HTTPException as e:
            raise e
        except Exception as e:
            print("Unexpected Error:", str(e))  # Print error for debugging
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def get_users(db: Session = Depends(get_db)):
        try:
            users = db.query(User).all()
            users_data = [{"email": user.email, "name": user.name, "mobile": user.mobile} for user in users]
            return {"total_users": len(users), "users": users_data}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


    def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
        try:
            user = db.query(User).filter(User.email == data.email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            if data.new_password != data.confirm_password:
                raise HTTPException(status_code=400, detail="Passwords do not match")

            hashed_password = hash_password(data.new_password)
            user.password = hashed_password
            db.commit()
            return {"message": "Password updated successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def delete_user(email: str, db: Session = Depends(get_db)):
        try:
            user = db.query(User).filter(User.email == email).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

    def protected_route(email: str = Depends(verify_token)):
        return {"message": f"Hello, {email}! This is a protected route."}


    def refresh_token(refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM], options={"verify_exp": False})
            print(payload)
            email = payload.get("email")
            if email is None:
                raise HTTPException(status_code= 401, detail="Invalid refresh token ")

            new_access_token = create_access_token(data={"sub": email})
            return {"access_token" : new_access_token, "token_type": "bearer"}
        except jwt.JWTError:
            raise HTTPException(status_code = 401, detail="Internal Server Error:")


