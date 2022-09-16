from sqlalchemy import Column, Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from src.database import Base
from src.model.unique_constraints import family_name_unique_constraint

class Family(Base):
    __tablename__: str = "family"
    __table_args__: tuple = (family_name_unique_constraint, )      
    parent_child_id: int = Column(
        "parent_child_id",
        Integer,
        ForeignKey(column="parent_child.id"),
        nullable=False
    )
    name: str = Column("name", VARCHAR(length=8), nullable=False)
    parent_child = relationship("ParentChild", back_populates="family")
    
