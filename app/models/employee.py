from sqlalchemy import (
    Column,
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import (relationship, backref)

from app.database import Base
from app.models.template import gen_utc_now, gen_created_at_column, gen_updated_at_column


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    hired_on = Column(DateTime, default=gen_utc_now)
    department_id = Column(Integer, ForeignKey('department.id'))
    department = relationship(
        "Department",
        backref=backref(
            'employees',
            uselist=True,
            cascade='delete,all',
        )
    )
    created_at = gen_created_at_column()
    updated_at = gen_updated_at_column()
