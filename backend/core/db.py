from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# ✅ FORCE LOAD .env FIRST
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path, override=True)

# ✅ Import config AFTER loading .env
from core.config import settings

DATABASE_URL = settings.DATABASE_URL

print("=" * 70)
print("✅ DB ENGINE USING:")
print(f"DATABASE_URL: {DATABASE_URL[:60]}...")
print("=" * 70)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "keepalives": 1,
        "keepalives_idle": 30,
        "keepalives_interval": 10,
        "keepalives_count": 5,
    } if DATABASE_URL.startswith("postgresql") else {}
)

def create_db_and_tables():
    try:
        print("Creating database tables...")
        print(f"Registered tables: {list(SQLModel.metadata.tables.keys())}")
        SQLModel.metadata.create_all(engine)
        print("✅ Database tables created successfully")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        raise

def get_session():
    with Session(engine) as session:
        yield session