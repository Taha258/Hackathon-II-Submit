"""
Seed Test User Script
Creates a test user in the database for development/testing
Uses bcrypt for password hashing (compatible with Better Auth)
"""

from sqlmodel import Session, select
from passlib.context import CryptContext
from core.db import engine, create_db_and_tables
from models import User, Account
import uuid

# Password hashing context - MUST use bcrypt for Better Auth compatibility
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed_test_user():
    """Create a test user for development"""
    
    print("🔧 Creating database tables...")
    # Create tables first
    create_db_and_tables()
    print("✅ Database tables created/verified")
    
    with Session(engine) as session:
        # Check if user already exists
        print("\n🔍 Checking if test user exists...")
        statement = select(User).where(User.email == "test@example.com")
        existing_user = session.exec(statement).first()
        
        if existing_user:
            print("✅ Test user already exists!")
            print(f"   Email: test@example.com")
            print(f"   Password: password123")
            print(f"   User ID: {existing_user.id}")
            return
        
        # Create user
        print("\n🔧 Creating test user...")
        user_id = str(uuid.uuid4())
        user = User(
            id=user_id,
            name="Test User",
            email="test@example.com",
            emailVerified=True
        )
        session.add(user)
        session.flush()  # ✅ IMPORTANT: Flush user first so it gets an ID
        
        # Create account with bcrypt hashed password
        print("🔐 Hashing password with bcrypt...")
        hashed_password = pwd_context.hash("password123")
        account = Account(
            id=str(uuid.uuid4()),
            accountId="test@example.com",
            providerId="credential",
            userId=user_id,
            password=hashed_password
        )
        session.add(account)
        
        # Commit to database
        print("💾 Saving to database...")
        session.commit()
        
        print("\n" + "="*60)
        print("✅ Test user created successfully!")
        print("="*60)
        print(f"   Email: test@example.com")
        print(f"   Password: password123")
        print(f"   User ID: {user_id}")
        print("="*60)
        print("\n💡 Use these credentials to login to the application")

if __name__ == "__main__":
    try:
        seed_test_user()
    except Exception as e:
        print(f"\n❌ Error creating test user: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if .env file exists with correct DATABASE_URL")
        print("   2. Verify database connection")
        print("   3. Ensure all packages are installed: pip install -r requirements.txt")
        import sys
        sys.exit(1)