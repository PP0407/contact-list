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


@app.route('/admin')
def admin():
    contacts = Contact.query.all()
    rows = ''.join(
        f'<tr><td>{c.id}</td><td>{c.name}</td><td>{c.phone}</td><td>{c.email}</td></tr>'
        for c in contacts
    )
    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Admin - Contacts</title>
        <style>
            body {{ font-family: Segoe UI, sans-serif; padding: 40px; background: #f0f2f5; }}
            h1 {{ color: #2c3e50; margin-bottom: 20px; }}
            table {{ border-collapse: collapse; width: 100%; background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
            th {{ background: #3498db; color: white; padding: 12px 16px; text-align: left; }}
            td {{ padding: 12px 16px; border-bottom: 1px solid #eee; }}
            tr:last-child td {{ border-bottom: none; }}
            tr:hover td {{ background: #f8f9fa; }}
            .count {{ margin-bottom: 16px; color: #666; }}
        </style>
    </head>
    <body>
        <h1>Contact List — Admin</h1>
        <p class="count">Total contacts: {len(contacts)}</p>
        <table>
            <thead><tr><th>ID</th><th>Name</th><th>Phone</th><th>Email</th></tr></thead>
            <tbody>{rows if rows else '<tr><td colspan="4" style="text-align:center;color:#999">No contacts yet</td></tr>'}</tbody>
        </table>
    </body>
    </html>
    '''
    return html


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
