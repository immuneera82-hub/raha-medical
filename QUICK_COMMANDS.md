# ⚡ أوامر سريعة للتنفيذ - Raha Medical
# Quick Commands Cheat Sheet

## 🚀 النشر السريع (Quick Deployment)

### استخدام السكريبت التلقائي:
```powershell
# في PowerShell
cd C:\Users\TOSHIBA\Desktop\RM
.\deploy.ps1
```

---

## 📝 الأوامر اليدوية (Manual Commands)

### 1. التحقق من الحالة
```powershell
# التحقق من Git status
git status

# التحقق من الفروع
git branch

# التحقق من الملفات السرية
git ls-files | Select-String ".env"
```

### 2. إضافة وحفظ التغييرات
```powershell
# إضافة جميع الملفات
git add .

# أو إضافة ملفات محددة
git add backend/static/templates/terms.html
git add backend/static/templates/faq.html
git add .gitignore
git add README.md

# Commit
git commit -m "✨ تحديثات الشفافية والامتثال القانوني"

# أو Commit مع رسالة مفصلة
git commit -m "✨ تحديثات الشفافية والامتثال القانوني

- حذف سياسة الإلغاء والاسترداد
- تعديل القانون المعمول به (الهند فقط)
- توضيح أن التكاليف تقديرية
- تحسين الأمان والحماية
- إضافة وثائق شاملة"
```

### 3. رفع على GitHub
```powershell
# رفع مباشر
git push origin main

# في حالة وجود تعارضات
git pull origin main --rebase
git push origin main

# فرض الرفع (احذر!)
git push origin main --force
```

---

## 🖥️ أوامر السيرفر (Server Commands)

### الاتصال بالسيرفر
```bash
# SSH (استبدل القيم بقيمك)
ssh user@rahamedical.com
# أو
ssh -i /path/to/key.pem user@server-ip
```

### التحديث على السيرفر
```bash
# 1. الانتقال للمجلد
cd /path/to/raha-medical

# 2. سحب التحديثات
git pull origin main

# 3. إعادة بناء Docker (طريقة كاملة)
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# أو إعادة تشغيل سريعة
docker-compose restart backend
```

### متابعة السجلات
```bash
# عرض آخر السجلات
docker-compose logs --tail=100

# متابعة مباشرة
docker-compose logs -f

# متابعة خدمة معينة
docker-compose logs -f backend
docker-compose logs -f caddy

# الخروج: Ctrl+C
```

---

## 🐳 أوامر Docker (Docker Commands)

### الحالة والمعلومات
```bash
# عرض الحاويات النشطة
docker-compose ps
# أو
docker ps

# عرض جميع الحاويات
docker ps -a

# عرض استخدام الموارد
docker stats

# عرض الصور
docker images
```

### التشغيل والإيقاف
```bash
# تشغيل جميع الخدمات
docker-compose up -d

# إيقاف جميع الخدمات
docker-compose down

# إعادة تشغيل
docker-compose restart

# إعادة تشغيل خدمة معينة
docker-compose restart backend
docker-compose restart caddy
```

### البناء والتنظيف
```bash
# إعادة البناء
docker-compose build

# بناء بدون كاش
docker-compose build --no-cache

# تنظيف الحاويات المتوقفة
docker container prune

# تنظيف الصور غير المستخدمة
docker image prune

# تنظيف شامل (احذر!)
docker system prune -a
```

### الدخول إلى الحاويات
```bash
# الدخول إلى Backend
docker-compose exec backend bash
# أو
docker-compose exec backend sh

# الدخول إلى Caddy
docker-compose exec caddy sh

# تنفيذ أمر داخل الحاوية
docker-compose exec backend python --version
```

---

## 🔧 أوامر Caddy (Caddy Commands)

```bash
# إعادة تحميل الإعدادات بدون توقف
docker-compose exec caddy caddy reload --config /etc/caddy/Caddyfile

# التحقق من صحة Caddyfile
docker-compose exec caddy caddy validate --config /etc/caddy/Caddyfile

# عرض الإعدادات الحالية
docker-compose exec caddy caddy run --config /etc/caddy/Caddyfile --dry-run
```

---

## 🔍 أوامر الاختبار والفحص (Testing Commands)

### اختبار الموقع
```bash
# اختبار الصفحة الرئيسية
curl https://rahamedical.com

# اختبار API health
curl https://api.rahamedical.com/health

# اختبار بتفاصيل أكثر
curl -I https://rahamedical.com

# اختبار HTTPS
curl -vI https://rahamedical.com 2>&1 | grep -i ssl
```

### فحص الشهادات
```bash
# عرض معلومات الشهادة
openssl s_client -connect rahamedical.com:443 -servername rahamedical.com

# التحقق من تاريخ انتهاء الصلاحية
echo | openssl s_client -servername rahamedical.com -connect rahamedical.com:443 2>/dev/null | openssl x509 -noout -dates
```

---

## 💾 أوامر النسخ الاحتياطي (Backup Commands)

```bash
# نسخة احتياطية من الملفات
tar -czf backup_$(date +%Y%m%d_%H%M%S).tar.gz backend/

# نسخة احتياطية من قاعدة البيانات Supabase
# (عادة يتم من لوحة تحكم Supabase)

# نقل النسخة لمكان آمن
mv backup_*.tar.gz /backups/
# أو
rsync -avz backup_*.tar.gz user@backup-server:/backups/
```

---

## 🔐 أوامر الأمان (Security Commands)

### فحص الملفات السرية
```powershell
# Windows PowerShell
git ls-files | Select-String ".env|credentials|\.key|\.pem"
```

```bash
# Linux/Mac
git ls-files | grep -E "\.env|credentials|\.key|\.pem"
```

### إزالة ملف سري من Git
```bash
# إزالة من Git فقط (يبقى على الجهاز)
git rm --cached .env
git rm --cached credentials.txt

# Commit التغيير
git commit -m "Remove sensitive files"

# رفع
git push origin main
```

### فحص الثغرات
```bash
# فحص المكتبات Python
pip install safety
safety check

# تحديث المكتبات
pip install --upgrade -r requirements.txt
```

---

## 📊 أوامر المراقبة (Monitoring Commands)

```bash
# عرض استخدام القرص
df -h

# عرض استخدام الذاكرة
free -m

# عرض العمليات
top
# أو
htop

# عرض استخدام Docker
docker stats

# عرض حجم الحاويات
docker ps -s

# عرض Log files
tail -f /var/log/caddy/access.log
tail -f /var/log/caddy/error.log
```

---

## 🆘 أوامر حل المشاكل (Troubleshooting)

### المشكلة: الحاويات لا تعمل
```bash
# 1. فحص السجلات
docker-compose logs backend

# 2. فحص الحالة
docker-compose ps

# 3. إعادة البناء الكامل
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### المشكلة: المنفذ مستخدم
```bash
# Linux
netstat -tuln | grep :5000
# أو
lsof -i :5000

# إيقاف العملية
kill -9 <PID>
```

```powershell
# Windows
netstat -ano | findstr :5000

# إيقاف العملية
taskkill /PID <PID> /F
```

### المشكلة: مشاكل في الصلاحيات
```bash
# إعطاء صلاحيات للسكريبتات
chmod +x deploy.sh

# إصلاح صلاحيات الملفات
chown -R user:user /path/to/raha-medical
```

---

## 📌 أوامر إضافية مفيدة

### Git
```bash
# إلغاء آخر commit (مع الاحتفاظ بالتغييرات)
git reset --soft HEAD~1

# إلغاء آخر commit (حذف التغييرات)
git reset --hard HEAD~1

# عرض سجل التغييرات
git log --oneline --graph --all

# عرض الفروق
git diff

# حفظ التغييرات مؤقتاً
git stash
git stash pop
```

### Python
```bash
# تفعيل البيئة الافتراضية
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows

# تثبيت المكتبات
pip install -r requirements.txt

# تجميد المكتبات
pip freeze > requirements.txt

# تشغيل Flask محلياً
python app.py
# أو
flask run
```

---

## 🎯 سير العمل المعتاد (Typical Workflow)

### تطوير محلي:
```powershell
# 1. سحب آخر التحديثات
git pull origin main

# 2. عمل التعديلات اللازمة

# 3. اختبار محلياً
docker-compose up -d

# 4. Commit و Push
git add .
git commit -m "وصف التغييرات"
git push origin main
```

### نشر على السيرفر:
```bash
# 1. SSH إلى السيرفر
ssh user@rahamedical.com

# 2. سحب التحديثات
cd /path/to/raha-medical
git pull origin main

# 3. إعادة تشغيل
docker-compose restart

# 4. التحقق
docker-compose logs -f
```

---

## 📞 للمساعدة

- **الوثائق الكاملة:** راجع `README.md`
- **دليل النشر:** راجع `DEPLOYMENT_GUIDE.md`
- **الأمان:** راجع `SECURITY_RECOMMENDATIONS.md`
- **الملخص:** راجع `UPDATE_SUMMARY.md`

---

**آخر تحديث:** ديسمبر 2024  
**الإصدار:** 1.0
