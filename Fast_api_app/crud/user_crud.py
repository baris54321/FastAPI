# perform user CRUD operations
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserUpdate

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


def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: int) -> bool:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return False
    db.delete(db_user)
    db.commit()
    return True

def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


def admin_approve_user(db: Session, user_id: int) -> User:
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        return None
    db_user.is_admin_approved = True
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_active_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_active == True).all()

def get_all_admin_approved_users(db: Session) -> list[User]:
    return db.query(User).filter(User.is_admin_approved == True).all()


