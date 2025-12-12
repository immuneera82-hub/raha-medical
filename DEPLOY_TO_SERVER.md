# 🚀 رفع التحديثات للسيرفر - Hostinger

## الخطوات الكاملة

### 1️⃣ رفع الكود إلى GitHub

```powershell
# في Terminal الخاص بـ Windows
cd C:\Users\TOSHIBA\Desktop\RM

# Add all changes
git add .

# Commit with descriptive message
git commit -m "feat: Enhanced Hospitals Section - Desktop static view, Mobile marquee, Artemis hospital profile with Quanta Chrome Laser"

# Push to GitHub
git push origin main
```

---

### 2️⃣ SSH إلى السيرفر

```powershell
ssh root@srv941562
```

**أو** إذا كان لديك اسم مستخدم مختلف:
```powershell
ssh your_username@srv941562
```

---

### 3️⃣ على السيرفر - تحديث الكود

```bash
# Navigate to project directory
cd ~/raha-medical

# Pull latest changes from GitHub
git pull origin main

# Should see:
# Updating abc1234..def5678
# Fast-forward
#  backend/main.py | 10 ++++++++--
#  backend/static/templates/index.html | 150 ++++++++++++++++++++++++++++++
#  ...
```

---

### 4️⃣ إعادة بناء وتشغيل Docker

```bash
# Stop current containers
docker-compose down

# Rebuild and start (this applies all changes)
docker-compose up -d --build

# Verify containers are running
docker ps
```

**يجب أن ترى** شيئاً مثل:
```
CONTAINER ID   IMAGE                    STATUS         PORTS
abc123def456   raha-medical-backend     Up 10 seconds  0.0.0.0:8000->8000/tcp
```

---

### 5️⃣ التحقق من Logs

```bash
# Check backend logs
docker logs raha-medical-backend-1 --tail 50

# Or follow logs in real-time
docker logs -f raha-medical-backend-1
```

**ابحث عن**:
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**وليس**:
```
ERROR: ...
```

---

### 6️⃣ اختبار الموقع المباشر

افتح المتصفح:
```
https://rahamedical.com
```

#### تحقق من:
1. ✅ قسم المستشفيات يظهر
2. ✅ Desktop: صف ثابت (لا يتحرك)
3. ✅ Mobile: marquee يتحرك لليمين
4. ✅ النقر على Artemis → `/knowledge-base/hospital/artemis`
5. ✅ صفحة Artemis تعرض:
   - نبذة عن المستشفى
   - JCI Badge
   - قسم "أحدث التقنيات" مع Quanta Chrome Laser
   - معرض الصور (3 صور)

---

## 🔧 استكشاف الأخطاء على السيرفر

### المشكلة: Container لا يبدأ

```bash
# Check container status
docker ps -a

# If status is "Exited", check logs
docker logs raha-medical-backend-1

# Common fix: Rebuild from scratch
docker-compose down -v
docker-compose up -d --build --force-recreate
```

---

### المشكلة: البيانات لا تظهر

```bash
# Enter the container
docker exec -it raha-medical-backend-1 bash

# Inside container, run Python verification
python -m backend.automation.verify_hospitals

# You should see:
# Count: 6
# - artemis (Artemis Hospitals) Partner=True
# - medanta (Medanta) Partner=True
# ...
```

**إذا كان Count: 0**:
البيانات غير موجودة في Supabase. تحقق من أنك شغّلت SQL في Supabase Dashboard.

---

### المشكلة: الصور لا تظهر

```bash
# Check if images exist
docker exec -it raha-medical-backend-1 ls -la backend/static/images/

# Should see:
# artemis_tech_1.jpg
# artemis_tech_2.jpg
# artemis_tech_3.jpg
# Artemis.png
# Medanta.png
# ...
```

**إذا لم توجد**: انسخها للسيرفر:
```bash
# On your local machine
scp backend/static/images/artemis_tech_*.jpg root@srv941562:~/raha-medical/backend/static/images/
```

---

### المشكلة: Caddy لا يعرض التحديثات

```bash
# Restart Caddy
docker restart caddy

# Or reload Caddy configuration
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

---

## 📊 التحقق النهائي

### في Terminal على السيرفر:

```bash
# Test backend API
curl http://localhost:8000/

# Test hospitals endpoint
curl http://localhost:8000/knowledge-base/hospital/artemis

# Should return HTML (not 404)
```

### في المتصفح:

```
https://rahamedical.com
```

1. افتح Developer Tools (F12)
2. Console Tab - يجب ألا يكون هناك أخطاء
3. Network Tab - تحقق من:
   - ✅ Status: 200 OK
   - ✅ hospitals data in response

---

## ⚡ الأوامر السريعة (نسخ ولصق)

```bash
# Full deployment sequence
cd ~/raha-medical && \
git pull origin main && \
docker-compose down && \
docker-compose up -d --build && \
docker ps && \
echo "✅ Deployment complete! Check https://rahamedical.com"
```

---

## 🎯 ملخص سريع

| الأمر | الغرض |
|------|-------|
| `git pull origin main` | جلب آخر التحديثات |
| `docker-compose down` | إيقاف الـ containers |
| `docker-compose up -d --build` | بناء وتشغيل |
| `docker ps` | التحقق من الـ containers |
| `docker logs -f <container>` | مشاهدة الـ logs |
| `docker exec -it <container> bash` | دخول الـ container |

---

## 🔐 ملاحظات أمان

- ✅ البيانات في Supabase (آمنة)
- ✅ الصور في `/static/` (public)
- ✅ الـ .env لا يتم رفعه لـ GitHub (gitignore)
- ✅ Supabase credentials على السيرفر فقط

---

جاهز للتطبيق؟ ابدأ من **الخطوة 1** ⬆️
