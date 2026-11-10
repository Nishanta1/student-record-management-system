import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'student_rms_super_secret_key_2026')
    
    # Database connection URL:
    # Supports PostgreSQL (Neon, Supabase, Aiven), MySQL, or local SQLite
    DB_URL = os.environ.get('DATABASE_URL', 'sqlite:///student_records.db')
    
    # Fix for SQLAlchemy 1.4+ where postgres:// must be postgresql://
    if DB_URL.startswith("postgres://"):
        DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = DB_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
