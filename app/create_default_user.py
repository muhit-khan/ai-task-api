import os
import sys

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
        
        # Create default user
        hashed_password = get_password_hash("admin")
        default_user = User(
            username="admin",
            email="admin@example.com",
            full_name="Administrator",
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