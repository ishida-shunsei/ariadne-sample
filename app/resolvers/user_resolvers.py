from app.database import get_db_session
from app.models import User


def resolve_users(_, info, id, name):
    session = get_db_session()
    query = session.query(User)
    if id is not None:
        query = query.filter(User.id==id)
    if name:
        query = query.filter(User.name==name)
    users = query.all()
    return users


def resolve_create_user(_, info, input):
    session = get_db_session()
    user = User(**input)
    session.add(user)
    session.commit()
    return user


def resolve_update_user(_, info, id, input):
    session = get_db_session()
    query = session.query(User).filter(User.id==id)
    if query.count() == 0:
        return None
    query.update(input)
    session.commit()
    return query.first()


def resolve_delete_user(_, info, id):
    session = get_db_session()
    user = session.query(User).get(id)
    if user is None:
        return False
    session.delete(user)
    session.commit()
    return True


__all__ = [
    "resolve_users",
    "resolve_create_user",
    "resolve_update_user",
    "resolve_delete_user",
]
