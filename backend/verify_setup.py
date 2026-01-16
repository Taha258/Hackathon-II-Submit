"""
Backend Setup Verification Script
Run this to verify everything is configured correctly before starting the server
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("🔍 Checking .env file...")
    
    if not Path(".env").exists():
        print("❌ .env file not found!")
        print("   Create it by copying .env.example")
        return False
    
    required_vars = [
        "DATABASE_URL",
        "BETTER_AUTH_SECRET",
        "SECRET_KEY",
    ]
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        missing = []
        for var in required_vars:
            if not os.getenv(var):
                missing.append(var)
        
        if missing:
            print(f"❌ Missing environment variables: {', '.join(missing)}")
            return False
        
        print("✅ .env file configured correctly")
        return True
    except Exception as e:
        print(f"❌ Error checking .env: {e}")
        return False


def check_database_connection():
    """Check if can connect to database"""
    print("\n🔍 Checking database connection...")
    
    try:
        from core.db import engine
        from sqlalchemy import text
        
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("   Check your DATABASE_URL in .env")
        return False


def check_tables():
    """Check if all required tables exist"""
    print("\n🔍 Checking database tables...")
    
    try:
        from core.db import engine
        from sqlalchemy import inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ["user", "account", "session", "tasks"]
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            print(f"❌ Missing tables: {', '.join(missing)}")
            print('   Run: python -c "from core.db import create_db_and_tables; create_db_and_tables()"')
            return False
        
        print(f"✅ All required tables exist: {', '.join(tables)}")
        return True
    except Exception as e:
        print(f"❌ Failed to check tables: {e}")
        return False


def check_test_user():
    """Check if test user exists"""
    print("\n🔍 Checking test user...")
    
    try:
        from sqlmodel import Session, select
        from core.db import engine
        from models import User
        
        with Session(engine) as session:
            statement = select(User).where(User.email == "test@example.com")
            user = session.exec(statement).first()
            
            if user:
                print(f"✅ Test user exists: {user.email}")
                print(f"   User ID: {user.id}")
                return True
            else:
                print("❌ Test user not found")
                print("   Run: python seed_user.py")
                return False
    except Exception as e:
        print(f"❌ Failed to check test user: {e}")
        return False


def check_dependencies():
    """Check if all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("sqlmodel", "sqlmodel"),
        ("psycopg2", "psycopg2"),
        ("jose", "jose"),
        ("passlib", "passlib"),
        ("pydantic_settings", "pydantic-settings"),
        ("dotenv", "python-dotenv"),
    ]
    
    missing = []
    for import_name, package_name in required_packages:
        try:
            __import__(import_name)
        except ImportError:
            missing.append(package_name)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed")
    return True


def main():
    """Run all verification checks"""
    print("=" * 60)
    print("🚀 Backend Setup Verification")
    print("=" * 60)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Database Connection", check_database_connection),
        ("Database Tables", check_tables),
        ("Test User", check_test_user),
    ]
    
    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"❌ {name} check failed with error: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 60)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 60)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print("=" * 60)
    
    if all(result for _, result in results):
        print("\n🎉 ALL CHECKS PASSED!")
        print("\n📝 Next steps:")
        print("   1. Start backend: uvicorn main:app --reload --port 8000")
        print("   2. Test API: http://localhost:8000")
        print("   3. View docs: http://localhost:8000/docs")
        print("   4. Setup frontend next")
        print("\n✅ Backend is ready to run!")
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("\n🔧 Fix the issues above and run this script again")
        print("\n💡 Common fixes:")
        print("   - pip install -r requirements.txt")
        print("   - Create .env file with DATABASE_URL")
        print("   - python -c \"from core.db import create_db_and_tables; create_db_and_tables()\"")
        print("   - python seed_user.py")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)