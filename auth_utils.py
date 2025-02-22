from passlib.context import CryptContext

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify if the entered password matches the stored hashed password."""
    return pwd_context.verify(plain_password, hashed_password)
