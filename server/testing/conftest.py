import pytest
from server.app import app
from server.models import db

@pytest.fixture(scope='session')
def app_context():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        try:
            yield app
        finally:
            db.session.remove()
            db.drop_all()
            db.session.close()

@pytest.fixture
def client(app_context):
    return app_context.test_client()

