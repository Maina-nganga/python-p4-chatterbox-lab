from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from flask_migrate import Migrate

from server.models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)
db.init_app(app)





@app.route('/messages', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    return jsonify([m.to_dict() for m in messages])



@app.route('/messages/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get_or_404(id)
    return jsonify(message.to_dict())




@app.route('/messages', methods=['POST'])
def create_message():
    data = request.get_json()
    if not data or 'body' not in data or 'username' not in data:
        return jsonify({"error": "Missing body or username"}), 400

    message = Message(body=data['body'], username=data['username'])
    db.session.add(message)
    db.session.commit()
    return jsonify(message.to_dict()), 201




@app.route('/messages/<int:id>', methods=['PATCH'])
def update_message(id):
    message = Message.query.get_or_404(id)
    data = request.get_json()
    if not data or 'body' not in data:
        return jsonify({"error": "Missing body"}), 400

    message.body = data['body']
    db.session.commit()
    return jsonify(message.to_dict())



@app.route('/messages/<int:id>', methods=['DELETE'])
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    db.session.expire_all() 
    return '', 204


if __name__ == '__main__':
    app.run(port=5555)
