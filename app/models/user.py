from sqlalchemy import (
    Column,
    String,
    Integer,
)

from app.database import Base
from app.models.template import gen_created_at_column, gen_updated_at_column

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    last_name = Column(String)
    created_at = gen_created_at_column()
    updated_at = gen_updated_at_column()

