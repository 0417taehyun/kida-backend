from datetime import datetime

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    __tablename__: str
    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    created_at: datetime = Column("created_at", DateTime(timezone=True), nullable=False)
    updated_at: datetime = Column("updated_at", DateTime(timezone=True), nullable=True)
    deleted_at: datetime = Column("deleted_at", DateTime(timezone=True), nullable=True)
