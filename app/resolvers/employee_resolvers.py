from app.database import get_db_session
from app.models import Employee


def resolve_employees(_, info, id, name, hired_on):
    with get_db_session() as session:
        query = session.query(Employee)
        if id is not None:
            query = query.filter(Employee.id==id)
        if name:
            query = query.filter(Employee.name==name)
        if hired_on:
            query = query.filter(Employee.hired_on==hired_on)
        employees = query.all()
        return employees


def resolve_create_employee(_, info, input):
    with get_db_session() as session:
        employee = Employee(**input)
        session.add(employee)
        session.commit()
        return employee


def resolve_update_employee(_, info, id, input):
    with get_db_session() as session:
        query = session.query(Employee).filter(Employee.id==id)
        if query.count() == 0:
            return None
        query.update(input)
        session.commit()
        return query.first()


def resolve_delete_employee(_, info, id):
    with get_db_session() as session:
        employee = session.query(Employee).get(id)
        if employee is None:
            return False
        session.delete(employee)
        session.commit()
        return True

__all__ = [
    "resolve_employees",
    "resolve_create_employee",
    "resolve_update_employee",
    "resolve_delete_employee",
]
