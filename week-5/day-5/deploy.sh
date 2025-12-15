#!/bin/bash

echo "🚀 Pulling latest code..."
git pull

echo "🐳 Deploying..."
docker compose -f docker-compose.prod.yml up -d --build

echo "🧹 Cleaning..."
docker system prune -f

echo "✅ Deployment DONE!"
