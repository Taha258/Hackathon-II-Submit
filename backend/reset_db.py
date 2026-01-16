from core.db import engine
from sqlmodel import SQLModel
from models.user import User
from models.task import Task
from models.account import Account
from models.session import Session
from models.verification import Verification

def reset_database():
    """Drop and recreate all tables"""
    print("🗑️  Dropping all tables...")
    SQLModel.metadata.drop_all(engine)
    
    print("📦 Creating all tables...")
    SQLModel.metadata.create_all(engine)
    
    print("✅ Database reset complete!")

if __name__ == "__main__":
    reset_database()