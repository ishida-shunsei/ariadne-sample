from datetime import datetime

from factory.alchemy import SQLAlchemyModelFactory

from app.database import get_db_session
from app.models import Department, Employee, User

db_session = get_db_session()

# テストコードで利用する場合は接続先の更新のため
# 利用直前に import あるいは importlib.reload() すること

class DepartmentFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Department
        sqlalchemy_session = db_session

    name = 'Some department'


class EmployeeFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Employee
        sqlalchemy_session = db_session

    name = 'John Doe'
    hired_on = datetime.fromisoformat("2000-01-01T00:00:00+09:00")
    department_id = 1


class UserFactory(SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = db_session

    name = 'John'
    last_name = 'Doe'

