import pytest
import app
from app import create


@pytest.fixture(scope='session')
def create_app():
    app = create()
    app.testing = True
    return app, app.test_client()
