from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import get_user_by_username, create_user
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.core.security import verify_password
from app.core.jwt import create_access_token

def register_user(db: Session, user: UserCreate) -> UserOut:
    print("Registrando usuario:", user.dict())
    
    if get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already registered")

    db_user = create_user(db, user)
    return UserOut.model_validate(db_user, from_attributes=True)  # <-- aquí está la magia

def authenticate_user(db: Session, credentials: UserLogin):
    user = get_user_by_username(db, credentials.username)
    if not user or not verify_password(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return create_access_token({"sub": user.username})
