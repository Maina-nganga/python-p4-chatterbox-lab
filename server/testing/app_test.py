from datetime import datetime

from server.models import db, Message

class TestApp:
    '''Flask application in app.py'''

    def test_has_correct_columns(self, client):
        with client.application.app_context():
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

    def test_returns_list_of_json_objects_for_all_messages_in_database(self, client):
        '''returns a list of JSON objects for all messages in the database.'''
        with client.application.app_context():
            response = client.get('/messages')
            records = Message.query.all()

            for message in response.json:
                assert(message['id'] in [record.id for record in records])
                assert(message['body'] in [record.body for record in records])

    def test_creates_new_message_in_the_database(self, client):
        '''creates a new message in the database.'''
        with client.application.app_context():

            client.post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()

    def test_returns_data_for_newly_created_message_as_json(self, client):
        '''returns data for the newly created message as JSON.'''
        with client.application.app_context():

            response = client.post(
                '/messages',
                json={
                    "body":"Hello 👋",
                    "username":"Liza",
                }
            )

            assert(response.content_type == 'application/json')

            assert(response.json["body"] == "Hello 👋")
            assert(response.json["username"] == "Liza")

            h = Message.query.filter_by(body="Hello 👋").first()
            assert(h)

            db.session.delete(h)
            db.session.commit()


    def test_updates_body_of_message_in_database(self, client):
        '''updates the body of a message in the database.'''
        with client.application.app_context():

            m = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id
            body = m.body

            client.patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            g = Message.query.filter_by(body="Goodbye 👋").first()
            assert(g)

            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_returns_data_for_updated_message_as_json(self, client):
        '''returns data for the updated message as JSON.'''
        with client.application.app_context():

            m = Message(
                body="Hello 👋",
                username="Liza")
            db.session.add(m)
            db.session.commit()
            id = m.id
            body = m.body

            response = client.patch(
                f'/messages/{id}',
                json={
                    "body":"Goodbye 👋",
                }
            )

            assert(response.content_type == 'application/json')
            assert(response.json["body"] == "Goodbye 👋")

            g = Message.query.filter_by(body="Goodbye 👋").first()
            g.body = body
            db.session.add(g)
            db.session.commit()

    def test_deletes_message_from_database(self, client):
        '''deletes the message from the database.'''
        with client.application.app_context():

            hello_from_liza = Message(
                body="Hello 👋",
                username="Liza")
            
            db.session.add(hello_from_liza)
            db.session.commit()

            client.delete(
                f'/messages/{hello_from_liza.id}'
            )
            db.session.commit()
            db.session.remove()

            h = db.session.query(Message).get(hello_from_liza.id)
            assert(not h)
