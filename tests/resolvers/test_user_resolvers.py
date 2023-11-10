from starlette.testclient import TestClient
import pytest

from app.database import new_db_session
from app.models import User

from tests.libs.assertion import assert_model, assert_model_list
from tests.libs.application import app


@pytest.fixture(scope="function")
def users_in_db():
    from app import factories
    users = [
        factories.UserFactory(name="Taro", last_name="Okita"),
        factories.UserFactory(name="James", last_name="Colman"),
    ]
    factories.db_session.commit()

    yield users

    for obj in users:
        factories.db_session.delete(obj)

def test__resolve_user_returns_success(users_in_db):
    client = TestClient(app)
    gql = """
    query {
        users {
            id
            name
            lastName
        }
    }
    """
    response = client.post('/graphql', json={"query": gql})
    assert response.status_code == 200
    result = response.json()
    users = result["data"]["users"]
    assert len(users) == 2
    assert_model_list(users, users_in_db)


def test__resolve_create_user_returns_success():
    client = TestClient(app)
    gql = """
    mutation {
        createUser (input: {
            name: "Makoto"
            lastName: "Shibya"
        }) {
            id
            name
            lastName
        }
    }
    """
    response = client.post('/graphql', json={"query": gql})
    assert response.status_code == 200
    result = response.json()
    user = result["data"]["createUser"]
    db_session = new_db_session()
    model = db_session.query(User).get(user["id"])
    assert_model(user, model)


def test__resolve_update_user_returns_success(users_in_db):
    client = TestClient(app)
    gql = """
    mutation ($id: Int!) {
        updateUser (id: $id, input: {
            name: "Makoto"
            lastName: "Shibya"
        }) {
            id
            name
            lastName
        }
    }
    """
    response = client.post('/graphql', json={"query": gql, "variables": {"id": users_in_db[0].id}})
    assert response.status_code == 200
    result = response.json()
    user = result["data"]["updateUser"]
    assert user["id"] == users_in_db[0].id
    db_session = new_db_session()
    model = db_session.query(User).get(user["id"])
    assert_model(user, model)


def test__resolve_delete_user_returns_success(users_in_db):
    client = TestClient(app)
    gql = """
    mutation ($id: Int!) {
        deleteUser (id: $id)
    }
    """
    response = client.post('/graphql', json={"query": gql, "variables": {"id": users_in_db[0].id}})
    assert response.status_code == 200
    result = response.json()
    assert result["data"]["deleteUser"] == True
    db_session = new_db_session()
    model = db_session.query(User).get(users_in_db[0].id)
    assert model is None
