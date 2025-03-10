from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from utils.database import SessionLocal, get_db
from Users.models import User
from Users.schemas import UserSignup, UserLogin, ResetPassword, DeleteUser
from auth_utils import hash_password, verify_password, create_access_token, create_refresh_token, verify_token
from Users.services import UserService
import jwt
from jose import JWTError, jwt

router = APIRouter()

SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.CrdKYwmgazyXb2ZfxMsKLxkV44Lv9D4MQLUyaynuNdI"
ALGORITHM = "HS256"
class UserAPI:

    @router.post("/signup/")
    def signup(user: UserSignup, db: Session = Depends(get_db)):
        return UserService.signup_user(user, db)

    @router.post("/login/")
    def login(user: UserLogin, db: Session = Depends(get_db)):
        return UserService.login(user, db)

    @router.get("/get")
    def get_users(db: Session = Depends(get_db)):
        return UserService.get_users(db)

    @router.put("/reset-password/")
    def reset_password(data: ResetPassword, db: Session = Depends(get_db)):
        return UserService.reset_password(data, db)

    @router.delete("/delete-user/{email}")
    def delete_user(email: str, db: Session = Depends(get_db)):
        return UserService.delete_user(email, db)
    
    @router.get("/protected")
    def protected_route(email: str = Depends(verify_token)):
        return UserService.protected_route(email)

    @router.post("/refresh-token")
    def refresh_token(refresh_token: str):
        return UserService.refresh_token(refresh_token)