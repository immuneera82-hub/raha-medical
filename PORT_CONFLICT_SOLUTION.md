# حل مشكلة تعارض المنفذ 80 في Docker

## 🔴 المشكلة
```
ERROR: for caddy  Cannot start service caddy: failed to set up container networking: 
failed to bind host port 0.0.0.0:80/tcp: address already in use
```

## ✅ الحل

### الطريقة السريعة (استخدام السكريبت)

قم بتحميل وتشغيل السكريبت التلقائي:

```bash
# على السيرفر
cd /root/raha-medical
# انسخ السكريبت من جهازك المحلي أو قم بإنشائه
nano fix_port_conflict.sh
# الصق محتوى السكريبت
chmod +x fix_port_conflict.sh
./fix_port_conflict.sh
```

---

### الطريقة اليدوية (خطوة بخطوة)

#### 1️⃣ إيقاف الخدمات الحالية
```bash
cd /root/raha-medical
docker-compose down
```

#### 2️⃣ التحقق من المنفذ 80
```bash
# معرفة ما يستخدم المنفذ
sudo lsof -i :80
# أو
sudo netstat -tulpn | grep :80
```

#### 3️⃣ إيقاف جميع حاويات Docker
```bash
# عرض جميع الحاويات
docker ps -a

# إيقافها جميعاً
docker stop $(docker ps -aq)

# حذف الحاويات المتوقفة
docker container prune -f
```

#### 4️⃣ إيقاف الخدمات المتعارضة (إن وجدت)
```bash
# إيقاف nginx
sudo systemctl stop nginx
sudo systemctl disable nginx

# أو إيقاف apache
sudo systemctl stop apache2
sudo systemctl disable apache2
```

#### 5️⃣ تحديث الكود من GitHub
```bash
cd /root/raha-medical
git pull origin main
```

#### 6️⃣ إعادة بناء وتشغيل الحاويات
```bash
# تحديث صور Docker
docker-compose pull

# إعادة البناء والتشغيل
docker-compose up -d --build
```

#### 7️⃣ التحقق من الحالة
```bash
# عرض حالة الحاويات
docker-compose ps

# عرض سجلات Caddy
docker-compose logs -f caddy

# عرض سجلات Backend
docker-compose logs -f backend
```

---

## 🔍 استكشاف الأخطاء الإضافية

### إذا استمرت المشكلة:

#### التحقق من العمليات على المنفذ 80
```bash
sudo fuser -k 80/tcp
```

#### إعادة تشغيل Docker بالكامل
```bash
sudo systemctl restart docker
```

#### حذف جميع الحاويات والشبكات
```bash
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)
docker network prune -f
docker volume prune -f
```

---

## ✅ التحقق من النجاح

بعد التشغيل، يجب أن ترى:

```bash
docker-compose ps
```

النتيجة المتوقعة:
```
Name                    State    Ports
raha-medical_backend_1  Up       0.0.0.0:8000->8000/tcp
raha-medical_caddy_1    Up       0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp
```

اختبر الموقع:
```bash
curl -I http://localhost
curl -I https://rahamedical.com
```

---

## 📝 ملاحظات مهمة

1. **المنفذ 80** مطلوب لـ Caddy لخدمة HTTP
2. **المنفذ 443** مطلوب لـ HTTPS
3. تأكد من عدم وجود nginx أو apache يعمل على نفس المنفذ
4. **تحديث الكود** من GitHub قبل إعادة التشغيل للحصول على آخر التغييرات

---

## 🆘 إذا احتجت مساعدة

قم بتشغيل وإرسال نتائج:
```bash
docker-compose ps
docker-compose logs caddy --tail=50
sudo lsof -i :80
```
