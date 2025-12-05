const express = require('express');
const app = express();
const port = 3000;

// Get the container hostname (to identify which instance is responding)
const os = require('os');
const hostname = os.hostname();

app.get('/api/health', (req, res) => {
  res.json({
    message: 'Backend is running!',
    server: hostname,
    timestamp: new Date().toISOString()
  });
});

app.get('/api/hello', (req, res) => {
  res.json({
    message: 'Hello from backend!',
    server: hostname,
    timestamp: new Date().toISOString()
  });
});

app.listen(port, () => {
  console.log(`Backend server ${hostname} listening on port ${port}`);
});