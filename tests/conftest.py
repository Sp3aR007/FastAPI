from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.oauth2 import create_access_token
from app.main import app
from app.config import settings
from app.database import get_db, Base
from app import models
import pytest
from alembic import command

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine =create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)





# client = TestClient(app)
@pytest.fixture(scope="function")
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="function")
def client(session):
    def override_get_db():
   
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)    

@pytest.fixture
def test_user(client):
    user_data = {"email" : "user@example.com", "password" : "password"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email" : "user1@example.com", "password" : "password"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    # print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):

    return create_access_token({"user_id" : test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "2nd user title",
        "content": "2nd user content",
        "owner_id": test_user2['id']
    }]
    def create_post_model(post):
        return models.Post(**post)
    posts_map = map(create_post_model, posts_data)
    session.add_all(posts_map)
    session.commit()
    posts = session.query(models.Post).all()
    
    return posts