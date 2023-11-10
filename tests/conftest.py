import os
import pytest
import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session, close_all_sessions
from app import database


@pytest.fixture(scope="session", autouse=True)
def use_test_session():
    """テスト実行時のデータベースをテスト用のものに切り替える

    Yields:
        scoped_session: テスト用のscoped_session
    """
    # settings of test database
    TEST_DATABASE_FILE = "test_temp.sqlite3"
    TEST_DATABASE_URL = "sqlite:///" + TEST_DATABASE_FILE

    TEST_DATABASE_PATH = database.PROJECT_ROOT.joinpath(TEST_DATABASE_FILE)
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)

    engine = sqlalchemy.create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

    _scoped_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    database._scoped_session = _scoped_session

    # Create test database and tables
    import app.models
    app.models.Base.metadata.create_all(engine)

    # このセッションを使う必要はないが、終了処理までブロックするためにyieldしておく
    yield _scoped_session

    close_all_sessions()
    
    if os.path.exists(TEST_DATABASE_PATH):
        os.remove(TEST_DATABASE_PATH)
