// Helper methods for CRUD operations via Express backend endpoints

const API_BASE = '/api/resources';

export async function getResources() {
  const res = await fetch(API_BASE);
  if (!res.ok) throw new Error('Failed to fetch resources');
  return res.json();
}

export async function getResource(id) {
  const res = await fetch(`${API_BASE}/${id}`);
  if (!res.ok) throw new Error('Failed to fetch resource');
  return res.json();
}

export async function createResource(data) {
  const res = await fetch(API_BASE, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error('Failed to create resource');
  return res.json();
}

export async function updateResource(id, data) {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  if (!res.ok) throw new Error('Failed to update resource');
  return res.json();
}

export async function deleteResource(id) {
  const res = await fetch(`${API_BASE}/${id}`, {
    method: 'DELETE'
  });
  if (!res.ok) throw new Error('Failed to delete resource');
  return res.json();
}
