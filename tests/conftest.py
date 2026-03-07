import pytest
from testcontainers.postgres import PostgresContainer
from bloggr import create_app 
from bloggr import db as _db
from flask_security.utils import hash_password
from bloggr.models import User
from flask_security.utils import login_user

# Start the Postgres Container once for the entire test run
@pytest.fixture(scope="session")
def postgres_server():
    with PostgresContainer("postgres:16-alpine") as postgres:
        yield postgres

# Set app fixture to use the Docker container's URI.
@pytest.fixture
def app(postgres_server):
    # Get the dynamic connection string from the container.
    # e.g., postgresql+psycopg2://test:test@localhost:54321/test
    database_uri = postgres_server.get_connection_url()
    
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": database_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():         # Enters the Flask application context.
        _db.create_all()  # Setup tables for this specific test.
        yield app           # Yields the app instance to tests (pauses here while tests run).
        _db.session.remove()            # Cleans up the database session.
        _db.drop_all()    # Wipe tables so the next test starts clean.

@pytest.fixture
def db(app):
    return _db

@pytest.fixture
def client(app):            # Creates a test client (simulates HTTP requests to the Flask app).
    return app.test_client()

@pytest.fixture
def create_user(db):
    username, password, email, confirmed_at, fs_uniquifier = "test_username", "test_password", "testmail@gmail.com", "2026-01-21 13:00:22.479989+01", "acbc5Feafb4E6bc7b1ae6de5e07b2d89"
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password, email=email, confirmed_at=confirmed_at, fs_uniquifier=fs_uniquifier)
    db.session.add(user)
    db.session.commit()
    return username, password, user, email, confirmed_at, fs_uniquifier

@pytest.fixture
def create_user2(db):
    username2, password2, email2, confirmed_at2, fs_uniquifier2 = "test_username2", "test_password2", "testmail2@gmail.com", "2025-01-21 13:34:22.479989+01", "scbs3Feafb4E6bc7f2ae6de5e07b2d89"
    hashed_password2 = hash_password(password2)
    user2 = User(username=username2, password=hashed_password2, email=email2, confirmed_at=confirmed_at2, fs_uniquifier=fs_uniquifier2 )
    db.session.add(user2)
    db.session.commit()
    return username2, password2, user2, email2, confirmed_at2, fs_uniquifier2

class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, email="testmail@gmail.com", password="test_password"):
        return self._client.post(
            "/login",
            data={
                "email": email,
                "password": password
            },
            follow_redirects=True
        )

    def logout(self):
        return self._client.get("/logout", follow_redirects=True)

@pytest.fixture
def auth(client):
    return AuthActions(client)