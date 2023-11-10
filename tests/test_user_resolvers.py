from starlette.testclient import TestClient
import pytest
from ariadne.utils import convert_camel_case_to_snake
from tests.libs.application import app


@pytest.fixture(scope="function")
def users_data():
    from app import factories
    user1 = factories.UserFactory(name="Satoshi", last_name="Yamada")
    user2 = factories.UserFactory(name="Jhon", last_name="Colman")
    factories.db_session.commit()
    yield [user1, user2]


def test__playground():
    client = TestClient(app)
    response = client.get('/graphql')
    assert response.status_code == 200


def test__resolve_user_returns_success(users_data):
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
    assert_models(result["data"]["users"], users_data)

def assert_models(dicts: list[dict], models: list):
    assert len(dicts) == len(models), "Length of dicts and modesl are different."
    for i in range(len(dicts)):
        dict_obj = dicts[i]
        model = models[i]
        for camel_key, dict_value in dict_obj.items():
            # json 側の camel case の名前を snake case に変換
            snake_key = convert_camel_case_to_snake(camel_key)
            model_value = getattr(model, snake_key)
            assert dict_value == model_value, f"Value for [{snake_key}] of dict and model are different."
