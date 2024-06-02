from sqlalchemy.orm import Session

from model.mysql import User

def get_user_by_username(username, db: Session):
    return db.query(User).filter(User.username == username).first()

def add_user(user: User, db: Session):
    try:
        db.add(user)
        db.commit()
    except Exception:
        db.rollback()
