from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app.schemas.user_schema import UserCreate, UserLogin, UserOut
from app.services.user_service import register_user, authenticate_user
from app.models.user import User
from app.core.jwt import decode_token
from app.core.config import DATABASE_URL
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import Base

router = APIRouter()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user)

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    token = authenticate_user(db, credentials)
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=UserOut)
def get_profile(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_token(token)
        user = get_user_by_username(db, payload.get("sub"))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/health")
def health():
    return {"status": "ok"}
