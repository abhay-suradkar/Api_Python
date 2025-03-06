from passlib.context import CryptContext
from jwt import encode, decode
import jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Union
from utils.database import get_db
from sqlalchemy.orm import Session
from datetime import datetime,  timedelta
from fastapi.security import OAuth2PasswordBearer
from Users.models import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the entered password matches the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

#AuthenticationPythonAPI123
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.CrdKYwmgazyXb2ZfxMsKLxkV44Lv9D4MQLUyaynuNdI"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 5
REFRESH_TOKEN_EXPIRE_MINUTES = 1

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=5))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_refresh_token(data: dict, expires_delta: timedelta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta  # Use 'expires_delta' instead of 'expiress_delta'
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

data = {"sub": "static_user"}
# Create access token
access_token = create_access_token(data)
print("Access Token:", access_token)

# Create refresh token
refresh_token = create_refresh_token(data)
print("Refresh Token:", refresh_token)


def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
    
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token: No user found")    
        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

