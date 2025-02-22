from pydantic import BaseModel, EmailStr, constr

class UserSignup(BaseModel):
    name: constr(min_length=2, max_length=100)
    email: EmailStr
    mobile: constr(min_length=10, max_length=15)
    password: constr(min_length=6)
    confirm_password: constr(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: constr(min_length=6)

class ResetPassword(BaseModel):
    email: EmailStr
    new_password: constr(min_length=6)
    confirm_password: constr(min_length=6)

class DeleteUser(BaseModel):
    email: EmailStr
