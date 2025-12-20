#!/bin/bash
# Script to fix Docker port 80 conflict

echo "========================================="
echo "Fixing Docker Port 80 Conflict"
echo "========================================="

# Step 1: Stop current Docker compose services
echo ""
echo "Step 1: Stopping current Docker Compose services..."
cd /root/raha-medical
docker-compose down

# Step 2: Check what's using port 80
echo ""
echo "Step 2: Checking what's using port 80..."
sudo lsof -i :80 || echo "lsof not available, trying netstat..."
sudo netstat -tulpn | grep :80 || echo "No service found on port 80"

# Step 3: Stop all Docker containers
echo ""
echo "Step 3: Stopping all Docker containers..."
docker stop $(docker ps -aq) 2>/dev/null || echo "No containers to stop"

# Step 4: Remove stopped containers
echo ""
echo "Step 4: Removing stopped containers..."
docker container prune -f

# Step 5: Check if nginx or apache is running
echo ""
echo "Step 5: Checking for nginx/apache services..."
sudo systemctl status nginx 2>/dev/null && sudo systemctl stop nginx
sudo systemctl status apache2 2>/dev/null && sudo systemctl stop apache2

# Step 6: Pull latest images
echo ""
echo "Step 6: Pulling latest Docker images..."
cd /root/raha-medical
git pull origin main
docker-compose pull

# Step 7: Start services
echo ""
echo "Step 7: Starting Docker Compose services..."
docker-compose up -d

# Step 8: Check status
echo ""
echo "Step 8: Checking service status..."
sleep 5
docker-compose ps

echo ""
echo "========================================="
echo "Done! Check the output above for any errors"
echo "========================================="
echo ""
echo "To view logs, run:"
echo "  docker-compose logs -f caddy"
echo "  docker-compose logs -f backend"
