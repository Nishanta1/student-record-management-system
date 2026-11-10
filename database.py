from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from config import Config
from models import Base

# Database engine initialization
connect_args = {}
if Config.SQLALCHEMY_DATABASE_URI.startswith('sqlite'):
    connect_args = {'check_same_thread': False}
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, connect_args=connect_args)
else:
    # Optimized connection parameters for remote PostgreSQL / MySQL
    engine = create_engine(
        Config.SQLALCHEMY_DATABASE_URI,
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True
    )

session_factory = sessionmaker(bind=engine)
db_session = scoped_session(session_factory)

def init_db():
    """Initializes tables and seeds base admin & sample accounts if not present."""
    Base.metadata.create_all(bind=engine)
    from seed_data import seed_database
    seed_database(db_session)
