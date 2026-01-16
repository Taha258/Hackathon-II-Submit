#backend\core\__init__.py
"""
Core package initialization
Exports commonly used functions and classes
"""

from .db import engine, create_db_and_tables, get_session
from .config import settings
from .security import hash_password, verify_password

__all__ = [
    # Database
    "engine",
    "create_db_and_tables",
    "get_session",
    
    # Config
    "settings",
    
    # Security
    "hash_password",
    "verify_password",
]
