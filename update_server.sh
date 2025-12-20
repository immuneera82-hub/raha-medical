#!/bin/bash
# Script to update Raha Medical server and clear all caches

echo "🚀 Starting server update..."

# 1. Pull latest code from GitHub
echo "📥 Pulling latest code..."
git reset --hard HEAD
git pull origin main

# 2. Restart services with Docker
echo "🔄 Restarting Docker containers..."
docker compose down
docker compose up -d --build

# 3. Clear Nginx/Caddy cache (if any)
# Caddy clears cache on restart, so step 2 handles it.

# 4. Message to user
echo "✅ Update complete!"
echo "⚠️ IMPORTANT: Please clear your browser cache (Ctrl+Shift+R) to see the changes."
