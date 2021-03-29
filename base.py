from flask_testing import TestCase
from feed_reader import app, db
from feed_reader.models import User


class BaseTestCase(TestCase):
    """A base test case."""

    def create_app(self):
        app.config['TESTING'] = True
        app.config['DEBUG'] = False
        return app

    def setUp(self):
        self.client = self.app.test_client()
        db.create_all()

    def tearDown(self):
        pass