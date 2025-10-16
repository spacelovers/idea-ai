from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
import jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
import os

router = APIRouter()

# تنظیمات امنیتی
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(BaseModel):
    id: str
    email: str
    full_name: str
    hashed_password: str
    is_active: bool = True
    created_at: datetime

class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

# دیتابیس موقت (در حالت واقعی از دیتابیس واقعی استفاده کنید)
fake_users_db = {}

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except jwt.JWTError:
        raise credentials_exception

    user = fake_users_db.get(email)
    if user is None:
        raise credentials_exception
    return user

@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    if user.email in fake_users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = get_password_hash(user.password)
    user_id = str(len(fake_users_db) + 1)

    new_user = User(
        id=user_id,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        created_at=datetime.utcnow()
    )

    fake_users_db[user.email] = new_user

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": new_user.id,
            "email": new_user.email,
            "full_name": new_user.full_name
        }
    }

@router.post("/login", response_model=Token)
async def login(user: UserLogin):
    db_user = fake_users_db.get(user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": db_user.id,
            "email": db_user.email,
            "full_name": db_user.full_name
        }
    }

@router.post("/google-auth")
async def google_auth(token: str):
    # اینجا باید با Google API ارتباط برقرار شود
    # برای سادگی، یک پیاده‌سازی ساده ارائه می‌دهیم
    try:
        # شبیه‌سازی احراز هویت گوگل
        # در حالت واقعی، token باید با Google API verify شود
        fake_google_user = {
            "email": "user@gmail.com",
            "name": "کاربر گوگل",
            "picture": "https://example.com/avatar.jpg"
        }

        # بررسی وجود کاربر در دیتابیس
        if fake_google_user["email"] not in fake_users_db:
            # ایجاد کاربر جدید
            user_id = str(len(fake_users_db) + 1)
            new_user = User(
                id=user_id,
                email=fake_google_user["email"],
                full_name=fake_google_user["name"],
                hashed_password="",  # برای کاربران گوگل پسورد نداریم
                created_at=datetime.utcnow()
            )
            fake_users_db[fake_google_user["email"]] = new_user

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": fake_google_user["email"]},
            expires_delta=access_token_expires
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "id": fake_users_db[fake_google_user["email"]].id,
                "email": fake_google_user["email"],
                "full_name": fake_google_user["name"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail="Google authentication failed")