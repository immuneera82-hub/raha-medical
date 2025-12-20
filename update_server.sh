#!/bin/bash
cd ~/raha-medical
git pull origin main
docker-compose down
docker system prune -af --volumes
docker-compose up -d --build --force-recreate
docker-compose logs -f
