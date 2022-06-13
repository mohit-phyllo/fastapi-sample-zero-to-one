from typing import Optional, List

from sqlalchemy.orm import Session

from app.db.models.model import User
from app.db.repository.base import BaseRepository


class UserRepository(BaseRepository[User]):

    # extra queries that can be over written
    def get_by_name(self, db: Session, name: str) -> Optional[List[User]]:
        return db.query(self.model).filter(self.model.name == name).all()


user_repository = UserRepository(User)
