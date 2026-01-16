import os
from pathlib import Path
from dotenv import load_dotenv

# Get absolute path to backend directory
BACKEND_DIR = Path(__file__).parent.parent
ENV_FILE = BACKEND_DIR / ".env"

# Load .env with absolute path
load_dotenv(dotenv_path=ENV_FILE, override=True)

# Debug
print("=" * 70)
print(f"🔍 Looking for .env at: {ENV_FILE}")
print(f"📁 .env exists: {ENV_FILE.exists()}")
if ENV_FILE.exists():
    print(f"📄 .env content preview:")
    with open(ENV_FILE, 'r') as f:
        for line in f.readlines()[:3]:
            if line.strip():
                key = line.split('=')[0]
                print(f"   {key}=...")
print("=" * 70)

class Settings:
    """Simple settings class"""
    
    def __init__(self):
        self.DATABASE_URL = os.getenv("DATABASE_URL")
        self.BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET", "")
        self.SECRET_KEY = os.getenv("SECRET_KEY", "")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "10080"))
        self.CORS_ORIGINS = ["https://hackathon-ii-front-end.vercel.app/"]
        
        if not self.DATABASE_URL:
            raise ValueError(f"DATABASE_URL not found! Check {ENV_FILE}")
        
        print("=" * 70)
        print("✅ CONFIG LOADED SUCCESSFULLY!")
        print(f"DATABASE_URL: {self.DATABASE_URL[:60]}...")
        print("=" * 70)

settings = Settings()