from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///contacts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'phone': self.phone, 'email': self.email}


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return jsonify({'status': 'Contact List API is running'})


@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    return jsonify([c.to_dict() for c in contacts])


@app.route('/contacts', methods=['POST'])
def add_contact():
    data = request.get_json()
    contact = Contact(name=data['name'], phone=data['phone'], email=data['email'])
    db.session.add(contact)
    db.session.commit()
    return jsonify(contact.to_dict()), 201


@app.route('/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    contact.name = data['name']
    contact.phone = data['phone']
    contact.email = data['email']
    db.session.commit()
    return jsonify(contact.to_dict())


@app.route('/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    db.session.delete(contact)
    db.session.commit()
    return jsonify({'message': 'Deleted'})


if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
