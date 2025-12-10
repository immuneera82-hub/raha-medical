#!/bin/bash
# server_debug.sh
# سكريبت لتشخيص مشاكل السيرفر
echo "=== 1. Checking Docker Containers ==="
docker-compose ps -a

echo -e "\n=== 2. Backend Logs (Last 50 lines) ==="
docker-compose logs --tail=50 backend

echo -e "\n=== 3. Testing Backend Connection Internal ==="
docker-compose exec backend curl -v http://localhost:8000/api/health

echo -e "\n=== End of Report ==="
