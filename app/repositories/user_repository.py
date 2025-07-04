from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password

def create_user(db: Session, user: UserCreate):
    hashed_pwd = hash_password(user.password)
    db_user = User(username=user.username, email=user.email, password_hash=hashed_pwd)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()
