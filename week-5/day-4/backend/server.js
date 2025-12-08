const express = require('express');
const app = express();
const port = 3000;
const os = require('os');

app.use(express.json());

app.get('/api/health', (req, res) => {
  const protocol = req.headers['x-forwarded-proto'] || req.protocol;
  res.json({
    status: 'healthy',
    server: os.hostname(),
    protocol: protocol,
    secure: protocol === 'https',
    timestamp: new Date().toISOString()
  });
});

app.get('/api/data', (req, res) => {
  res.json({
    message: 'Secure data transmission via HTTPS!',
    server: os.hostname(),
    data: {
      users: 150,
      revenue: '$50,000',
      status: 'operational'
    }
  });
});

app.post('/api/login', (req, res) => {
  res.json({
    message: 'Login processed securely',
    user: req.body.username || 'guest',
    encrypted: true
  });
});

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});