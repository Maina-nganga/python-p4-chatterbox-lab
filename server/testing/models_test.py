from datetime import datetime

from datetime import datetime

from server.models import db, Message

class TestMessage:
    '''Message model in models.py'''

    def test_has_correct_columns(self, app_context):
        with app_context.app_context():
            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            assert(hello_from_liza.body == "Hello 👋")
            assert(hello_from_liza.username == "Liza")
            assert(type(hello_from_liza.created_at) == datetime)

            db.session.delete(hello_from_liza)
            db.session.commit()
