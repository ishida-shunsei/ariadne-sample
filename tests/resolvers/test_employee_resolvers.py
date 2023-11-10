from datetime import datetime
from starlette.testclient import TestClient
import pytest

from tests.libs.assertion import assert_model_list
from tests.libs.application import app


@pytest.fixture(scope="function")
def employees_in_db():
    from app import factories
    dep1 = factories.DepartmentFactory(name="R&D")
    dep2 = factories.DepartmentFactory(name="Marketing")
    employee1 = factories.EmployeeFactory(
        name="Satoshi",
        hired_on=datetime.fromisoformat("2002-01-01T00:00:00+09:00"),
        department=dep1,
    )
    employee2 = factories.EmployeeFactory(
        name="Jhon",
        hired_on=datetime.fromisoformat("2023-02-03T00:00:00+09:00"),
        department=dep2,
    )
    factories.db_session.commit()
    yield [employee1, employee2]


def test__resolve_employees_returns_success(employees_in_db):
    client = TestClient(app)
    gql = """
    query {
        employees {
            id
            name
            hiredOn
            department {
                id
                name
            }
        }
    }
    """
    response = client.post('/graphql', json={"query": gql})
    assert response.status_code == 200
    result = response.json()
    employees = result["data"]["employees"]
    assert len(employees) == 2
    assert_model_list(employees, employees_in_db)
