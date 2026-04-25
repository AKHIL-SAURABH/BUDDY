import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from backend.core.config import settings

# Ensure the directory for the SQLite file actually exists
db_dir = os.path.dirname(settings.DATABASE_URL.replace("sqlite:///", ""))
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

# Create the SQLAlchemy Engine
# (check_same_thread is False because FastAPI can access the DB from different async workers)
engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for our declarative ORM models (if you add them later)
Base = declarative_base()

# Dependency to use in FastAPI routes
def get_db():
    """Yields a database session and safely closes it after the request finishes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()