#backend\api\routes\auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from jose import jwt, JWTError
from datetime import datetime, timedelta
from typing import Annotated
import os

from core.db import get_session
from core.security import hash_password, verify_password
from models import User, Account
from schemas import UserCreate, UserLogin, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Security
security = HTTPBearer()

# Environment variables
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

SessionDep = Annotated[Session, Depends(get_session)]


def create_access_token(user_id: str, email: str) -> str:
    """Create JWT access token"""
    expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow()
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """Verify JWT token and extract user info"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        return {"user_id": user_id, "email": payload.get("email")}
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


TokenDep = Annotated[dict, Depends(verify_token)]


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, session: SessionDep):
    """
    Register a new user
    
    - Creates user account
    - Hashes password
    - Returns JWT token
    """
    # Check if user already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = session.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    print("Password length:", len(user_data.password))
    # Create new user
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        email_verified=False
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    # Create account with hashed password
    hashed_pw = hash_password(user_data.password)
    account = Account(
        user_id=new_user.id,
        account_id=new_user.id,
        provider_id="credential",
        password=hashed_pw
    )
    session.add(account)
    session.commit()
    
    # Generate JWT token
    access_token = create_access_token(new_user.id, new_user.email)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=new_user.id,
            email=new_user.email,
            name=new_user.name
        )
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, session: SessionDep):
    """
    Login user
    
    - Verifies email and password
    - Returns JWT token
    """
    # Find user by email
    statement = select(User).where(User.email == credentials.email)
    user = session.exec(statement).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Get account with password
    account_statement = select(Account).where(
        Account.user_id == user.id,
        Account.provider_id == "credential"
    )
    account = session.exec(account_statement).first()
    
    if not account or not account.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, account.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    access_token = create_access_token(user.id, user.email)
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(
            id=user.id,
            email=user.email,
            name=user.name
        )
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user(session: SessionDep, token_data: TokenDep):
    """
    Get current authenticated user's information
    """
    user_id = token_data["user_id"]
    
    # Get user from database
    user = session.get(User, user_id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        name=user.name
    )