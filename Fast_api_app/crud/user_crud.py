# perform user CRUD operations
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate

def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        username=user.username,
        email=user.email,
    )
    db_user.set_password(user.password) 
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    user_dict = db_user.__dict__
    return user_dict

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def get_all_users(db: Session) -> list[User]:
    return db.query(User).filter(User.deleted_at.is_(None)).all()

def get_all_active_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_active == True).all()

def get_all_admin_approved_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_admin_approved == True).filter(User.deleted_at.is_(None)).all()

def get_unapproved_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_admin_approved == False).filter(User.deleted_at.is_(None)).all()

