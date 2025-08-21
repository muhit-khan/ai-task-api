import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the parent directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from app.database import User, get_db, create_db_and_tables
from app.services.auth_service import get_password_hash

def create_default_user():
    # Create database tables
    create_db_and_tables()
    
    # Get database session
    db_gen = get_db()
    db = next(db_gen)
    
    try:
        # Check if default user already exists
        existing_user = db.query(User).filter(User.username == "admin").first()
        if existing_user:
            print("Default user 'admin' already exists.")
            return
        
        # Get default user credentials from environment variables
        default_username = os.getenv("ADMIN_USERNAME", "admin")
        default_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
        default_full_name = os.getenv("ADMIN_FULL_NAME", "Administrator")
        default_password = os.getenv("ADMIN_PASSWORD", "admin")
        
        # Create default user
        hashed_password = get_password_hash(default_password)
        default_user = User(
            username=default_username,
            email=default_email,
            full_name=default_full_name,
            hashed_password=hashed_password
        )
        
        db.add(default_user)
        db.commit()
        db.refresh(default_user)
        print("Default user 'admin' created successfully.")
        
    except Exception as e:
        print(f"Error creating default user: {e}")
        db.rollback()
    finally:
        # Close database session
        try:
            db_gen.__next__()
        except StopIteration:
            pass

if __name__ == "__main__":
    create_default_user()