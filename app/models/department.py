from sqlalchemy import (
    Column,
    String,
    Integer,
)

from app.database import Base
from app.models.template import gen_created_at_column, gen_updated_at_column

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    place = Column(String(50), nullable=False)
    manager = Column(String(50), nullable=False)
    created_at = gen_created_at_column()
    updated_at = gen_updated_at_column()
