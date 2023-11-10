from app.database import get_db_session
from app.models import Department


def resolve_departments(_, info, id, name):
    session = get_db_session()
    query = session.query(Department)
    if id is not None:
        query = query.filter(Department.id==id)
    if name:
        query = query.filter(Department.name==name)
    departments = query.all()
    return departments


__all__ = [
    "resolve_departments",
]