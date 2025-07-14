// Express backend for EmberAI CRUD API
const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(bodyParser.json());

// In-memory store for demonstration (replace with DB in prod)
let resources = [];
let idCounter = 1;

// GET all resources
app.get('/api/resources', (req, res) => {
  res.json(resources);
});

// GET a single resource
app.get('/api/resources/:id', (req, res) => {
  const resource = resources.find(r => r.id === parseInt(req.params.id));
  if (!resource) return res.status(404).json({ error: 'Not found' });
  res.json(resource);
});

// CREATE a resource
app.post('/api/resources', (req, res) => {
  const resource = { id: idCounter++, ...req.body };
  resources.push(resource);
  res.status(201).json(resource);
});

// UPDATE a resource
app.put('/api/resources/:id', (req, res) => {
  const idx = resources.findIndex(r => r.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  resources[idx] = { ...resources[idx], ...req.body };
  res.json(resources[idx]);
});

// DELETE a resource
app.delete('/api/resources/:id', (req, res) => {
  const idx = resources.findIndex(r => r.id === parseInt(req.params.id));
  if (idx === -1) return res.status(404).json({ error: 'Not found' });
  const deleted = resources.splice(idx, 1);
  res.json(deleted[0]);
});

app.listen(PORT, () => {
  console.log(`EmberAI backend running on port ${PORT}`);
});
