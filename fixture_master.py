from datetime import datetime

from app import factories


def run_fixture():
    department_marketing = factories.DepartmentFactory(name="Marketing")
    department_supply = factories.DepartmentFactory(name="Supply")

    factories.EmployeeFactory(name="Ryan", hired_on=datetime.fromisoformat("2010-11-01T00:00:00"), department=department_marketing)
    factories.EmployeeFactory(name="Kevin", hired_on=datetime.fromisoformat("1999-06-16T00:00:00"), department=department_supply)

    factories.UserFactory(name="Satoshi", last_name="Yamada")
    factories.UserFactory(name="Jhon", last_name="Colman")
    factories.db_session.commit()


if __name__ == '__main__':
    run_fixture()
