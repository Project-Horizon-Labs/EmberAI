import React, { useEffect, useState } from 'react';
import {
  getResources,
  getResource,
  createResource,
  updateResource,
  deleteResource
} from './apiHelpers';

export default function ResourceCRUD() {
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [form, setForm] = useState({ name: '', description: '' });
  const [editingId, setEditingId] = useState(null);

  // Fetch all resources on mount
  useEffect(() => {
    refresh();
  }, []);

  function refresh() {
    setLoading(true);
    getResources()
      .then(setResources)
      .catch(setError)
      .finally(() => setLoading(false));
  }

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    try {
      if (editingId) {
        await updateResource(editingId, form);
      } else {
        await createResource(form);
      }
      setForm({ name: '', description: '' });
      setEditingId(null);
      refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleEdit(id) {
    try {
      const resource = await getResource(id);
      setForm({ name: resource.name || '', description: resource.description || '' });
      setEditingId(id);
    } catch (err) {
      setError(err.message);
    }
  }

  async function handleDelete(id) {
    if (!window.confirm('Delete this resource?')) return;
    try {
      await deleteResource(id);
      refresh();
    } catch (err) {
      setError(err.message);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', background: '#fff', borderRadius: 12, boxShadow: '0 2px 16px #dbeafe', padding: 32 }}>
      <h2 style={{ color: '#4a63ff', marginBottom: 16 }}>Resource CRUD Example</h2>
      <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 12, marginBottom: 24 }}>
        <input
          name="name"
          placeholder="Resource Name"
          value={form.name}
          onChange={handleChange}
          required
          style={{ padding: 8, borderRadius: 6, border: '1px solid #bcd', fontSize: 16 }}
        />
        <textarea
          name="description"
          placeholder="Description"
          value={form.description}
          onChange={handleChange}
          rows={2}
          style={{ padding: 8, borderRadius: 6, border: '1px solid #bcd', fontSize: 15 }}
        />
        <button type="submit" style={{ background: 'linear-gradient(90deg, #4a63ff 0%, #5eead4 100%)', color: '#fff', border: 'none', borderRadius: 6, padding: '8px 0', fontWeight: 600, fontSize: 17, cursor: 'pointer' }}>
          {editingId ? 'Update' : 'Create'} Resource
        </button>
        {editingId && (
          <button type="button" onClick={() => { setEditingId(null); setForm({ name: '', description: '' }); }} style={{ background: '#eee', color: '#222', border: 'none', borderRadius: 6, padding: '8px 0', fontWeight: 500, fontSize: 15, cursor: 'pointer' }}>
            Cancel Edit
          </button>
        )}
      </form>
      {error && <div style={{ color: 'red', marginBottom: 12 }}>{error}</div>}
      {loading ? (
        <div>Loading...</div>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {resources.map(r => (
            <li key={r.id} style={{ padding: '10px 0', borderBottom: '1px solid #e5e7eb', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <strong>{r.name}</strong>
                <div style={{ color: '#666', fontSize: 14 }}>{r.description}</div>
              </div>
              <div>
                <button onClick={() => handleEdit(r.id)} style={{ marginRight: 8, background: '#f1f5ff', color: '#4a63ff', border: 'none', borderRadius: 5, padding: '4px 10px', cursor: 'pointer', fontWeight: 500 }}>Edit</button>
                <button onClick={() => handleDelete(r.id)} style={{ background: '#fee2e2', color: '#d32f2f', border: 'none', borderRadius: 5, padding: '4px 10px', cursor: 'pointer', fontWeight: 500 }}>Delete</button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
