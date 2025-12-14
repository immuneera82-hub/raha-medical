#!/bin/bash

# 🔧 سكريبت تحديث السيرفر الكامل

echo "🚀 بدء تحديث السيرفر..."

# 1. الانتقال للمجلد
cd ~/raha-medical || exit 1
echo "✅ في مجلد المشروع"

# 2. سحب آخر التحديثات
echo "📥 سحب التحديثات من Git..."
git fetch origin
git pull origin main

# 3. إيقاف الخدمات
echo "⏸️ إيقاف Docker containers..."
docker-compose down

# 4. إعادة البناء والتشغيل
echo "🔨 إعادة بناء الصور..."
docker-compose build --no-cache backend

echo "▶️ تشغيل الخدمات..."
docker-compose up -d

# 5. انتظار 5 ثواني
echo "⏳ انتظار استعداد الخدمات..."
sleep 5

# 6. التحقق من الحالة
echo "🔍 التحقق من الحالة..."
docker ps

echo ""
echo "📊 Logs من Backend:"
docker logs raha-medical-backend-1 --tail 30

echo ""
echo "✅ تم التحديث!"
echo "🌐 جرب الآن: https://rahamedical.com/hospitals/artemis"
