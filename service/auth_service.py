from sqlalchemy.orm import Session

from crud.crud_user import get_user_by_username, add_user
from model.mysql import User


class AuthService:
    def check_user_exists(self, username, db: Session):
        user = get_user_by_username(username, db)
        if user:
            return user.to_dict()
        else:
            user = User(username=username)
            add_user(user, db)
            return user.to_dict()


auth_service = AuthService()