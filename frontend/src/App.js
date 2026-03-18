import { useState, useEffect } from 'react';
import './App.css';

const API = 'http://127.0.0.1:5000/contacts';

function App() {
  const [contacts, setContacts] = useState([]);
  const [form, setForm] = useState({ name: '', phone: '', email: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchContacts();
  }, []);

  const fetchContacts = async () => {
    const res = await fetch(API);
    const data = await res.json();
    setContacts(data);
  };

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (editingId) {
      await fetch(`${API}/${editingId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
      setEditingId(null);
    } else {
      await fetch(API, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      });
    }
    setForm({ name: '', phone: '', email: '' });
    fetchContacts();
  };

  const handleEdit = (contact) => {
    setEditingId(contact.id);
    setForm({ name: contact.name, phone: contact.phone, email: contact.email });
  };

  const handleDelete = async (id) => {
    await fetch(`${API}/${id}`, { method: 'DELETE' });
    fetchContacts();
  };

  const handleCancel = () => {
    setEditingId(null);
    setForm({ name: '', phone: '', email: '' });
  };

  return (
    <div className="container">
      <h1>Contact List</h1>

      <form onSubmit={handleSubmit} className="form">
        <input
          name="name"
          placeholder="Name"
          value={form.name}
          onChange={handleChange}
          required
        />
        <input
          name="phone"
          placeholder="Phone"
          value={form.phone}
          onChange={handleChange}
          required
        />
        <input
          name="email"
          placeholder="Email"
          value={form.email}
          onChange={handleChange}
          required
        />
        <div className="form-buttons">
          <button type="submit">{editingId ? 'Update' : 'Add Contact'}</button>
          {editingId && <button type="button" className="cancel" onClick={handleCancel}>Cancel</button>}
        </div>
      </form>

      <div className="contact-list">
        {contacts.length === 0 && <p className="empty">No contacts yet. Add one above.</p>}
        {contacts.map((c) => (
          <div key={c.id} className="contact-card">
            <div className="contact-info">
              <strong>{c.name}</strong>
              <span>{c.phone}</span>
              <span>{c.email}</span>
            </div>
            <div className="contact-actions">
              <button className="edit" onClick={() => handleEdit(c)}>Edit</button>
              <button className="delete" onClick={() => handleDelete(c.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
