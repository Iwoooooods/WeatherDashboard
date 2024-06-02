import time
from typing import List

from sqlalchemy import Column, Integer, DateTime, inspect, func, String, JSON
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.orm import declared_attr


@as_declarative()
class Base:
    id = Column(Integer, primary_key=True, nullable=False)
    create_at = Column(DateTime, server_default=func.now(), nullable=False)
    modify_at = Column(DateTime, server_default=None, nullable=True, onupdate=func.now())
    __name__: str

    # 自动生成表名，表名为类名的小写
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def to_dict(self) -> dict: # model转换字典，主要未来避免InstanceState字段出现
        return {
            c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs
        }

class User(Base):
    username: str = Column(String, unique=True, nullable=False)
    preference: List[str] = Column(JSON, server_default=None, nullable=True)


