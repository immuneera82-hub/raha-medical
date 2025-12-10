# 🛡️ توصيات الحماية والأمان لموقع Raha Medical

## 📅 تاريخ الإعداد: ديسمبر 2024

---

## 🔐 1. استراتيجية التشفير والحماية من المستوى العالي

### 1.1 تشفير البيانات
```yaml
✅ الإجراءات المطبقة حالياً:
  - HTTPS/TLS 1.3 عبر Caddy Server
  - تشفير البيانات في قاعدة البيانات (Supabase)
  - تشفير كلمات المرور باستخدام bcrypt

🔧 التحسينات المقترحة:
  - تفعيل HSTS (HTTP Strict Transport Security) headers
  - استخدام Certificate Pinning للتطبيقات المحمولة
  - تشفير end-to-end للملفات الطبية الحساسة
  - استخدام AES-256 لتشفير الملفات المخزنة
```

### 1.2 تشفير قاعدة البيانات
```python
# توصيات Supabase Security:
- تفعيل Row Level Security (RLS) على جميع الجداول ✅
- استخدام vault للبيانات الحساسة جداً (أرقام بطاقات الهوية)
- تشفير الحقول الحساسة قبل التخزين
- حذف البيانات القديمة بشكل دوري (Data Retention Policy)
```

---

## 📁 2. إدارة الملفات السرية والعامة

### 2.1 الملفات التي يجب أن تبقى سرية
```
🔴 سري للغاية (لا ترفع على GitHub مطلقاً):
├── .env                          # بيانات الاتصال بقواعد البيانات
├── raha-medical-credentials.txt # بيانات الحسابات
├── backend/keys/                 # مفاتيح التشفير والAPI
├── backend/ssl/                  # شهادات SSL الخاصة (إن وجدت)
└── backups/                      # نسخ احتياطية من قاعدة البيانات

🟡 سري (يمكن أن يكون على الخادم فقط):
├── docker-compose.yml            # قد يحتوي على معلومات حساسة
├── Caddyfile                     # إعدادات الخادم
└── backend/config/               # ملفات الإعدادات
```

### 2.2 الملفات الآمنة للنشر
```
🟢 آمن للنشر (Public):
├── backend/static/               # ملفات CSS, JS, الصور
├── backend/templates/            # قوالب HTML
├── README.md                     # وثائق المشروع
├── .gitignore                    # ✅ متأكد أنه يستثني الملفات السرية
└── requirements.txt              # المكتبات المطلوبة
```

### 2.3 التحقق من .gitignore
```bash
# تأكد من أن .gitignore يحتوي على:
.env
.env.*
*.key
*.pem
*.log
credentials.txt
secrets/
backups/
__pycache__/
*.pyc
node_modules/
.DS_Store
```

---

## 🚫 3. الحماية من النسخ والـ Screenshot

### 3.1 منع النسخ (Copy Protection)
```css
/* CSS للحماية من النسخ */
body {
    -webkit-user-select: none;
    -moz-user-select: none;
    -ms-user-select: none;
    user-select: none;
}

/* منع الضغط بالزر الأيمن */
body {
    -webkit-touch-callout: none;
}
```

```javascript
// JavaScript للحماية المتقدمة
// منع الضغط بالزر الأيمن
document.addEventListener('contextmenu', event => event.preventDefault());

// منع Ctrl+C, Ctrl+X
document.addEventListener('keydown', (e) => {
    if (e.ctrlKey && (e.key === 'c' || e.key === 'x' || e.key === 'u' || e.key === 's')) {
        e.preventDefault();
        return false;
    }
});

// منع السحب للصور
document.addEventListener('dragstart', (e) => {
    if (e.target.tagName === 'IMG') {
        e.preventDefault();
    }
});

// تشويش محتوى الصفحة عند التبديل للتطبيقات الأخرى (محتمل screenshot)
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        document.body.classList.add('blurred-content');
    } else {
        document.body.classList.remove('blurred-content');
    }
});
```

### 3.2 الحماية من Screenshot
```javascript
// ⚠️ ملاحظة مهمة:
// لا توجد طريقة تقنية 100% لمنع Screenshots في المتصفحات
// ولكن يمكن اتخاذ إجراءات لتقليل جودتها أو علامتها

// 1. Watermarking ديناميكي
function addDynamicWatermark() {
    const watermark = document.createElement('div');
    watermark.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 120px;
        color: rgba(0, 0, 0, 0.05);
        pointer-events: none;
        z-index: 9999;
        user-select: none;
    `;
    watermark.textContent = `${getUserEmail()} - ${new Date().toLocaleDateString()}`;
    document.body.appendChild(watermark);
}

// 2. Dynamic Background Pattern
function addAntiScreenshotPattern() {
    const canvas = document.createElement('canvas');
    canvas.width = 200;
    canvas.height = 200;
    const ctx = canvas.getContext('2d');
    
    // رسم نمط معقد بمعلومات المستخدم
    ctx.font = '10px Arial';
    ctx.fillStyle = 'rgba(0,0,0,0.02)';
    for(let i = 0; i < 20; i++) {
        ctx.fillText(getUserId(), Math.random() * 200, Math.random() * 200);
    }
    
    document.body.style.backgroundImage = `url(${canvas.toDataURL()})`;
}
```

### 3.3 حماية المحتوى الطبي الحساس
```javascript
// للملفات الطبية الحساسة جداً
// استخدام Canvas لعرض الصور بدلاً من <img>
function displaySecureImage(imageUrl, containerId) {
    const canvas = document.getElementById(containerId);
    const ctx = canvas.getContext('2d');
    const img = new Image();
    
    img.onload = function() {
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        
        // إضافة watermark مخفي
        ctx.font = '12px Arial';
        ctx.fillStyle = 'rgba(255,255,255,0.1)';
        ctx.fillText(`User: ${getUserId()} - ${new Date()}`, 10, 20);
    };
    
    img.src = imageUrl;
}
```

---

## 🛡️ 4. الحماية من استنساخ الموقع (Clone Protection)

### 4.1 حماية على مستوى الخادم
```python
# في Flask/FastAPI backend
from flask import request, abort

ALLOWED_ORIGINS = [
    'https://rahamedical.com',
    'https://www.rahamedical.com',
    'https://api.rahamedical.com'
]

@app.before_request
def verify_origin():
    origin = request.headers.get('Origin')
    referer = request.headers.get('Referer')
    
    # التحقق من Origin و Referer
    if origin and origin not in ALLOWED_ORIGINS:
        abort(403, "Unauthorized origin")
    
    # التحقق من User-Agent للكشف عن Scrapers
    user_agent = request.headers.get('User-Agent', '').lower()
    suspicious_agents = ['wget', 'curl', 'scraper', 'bot']
    if any(agent in user_agent for agent in suspicious_agents):
        # تسجيل المحاولة
        log_suspicious_activity(request)
        abort(403, "Suspicious activity detected")
```

### 4.2 Rate Limiting
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/api/<path:path>")
@limiter.limit("10 per minute")
def api_endpoint(path):
    # API endpoints
    pass
```

### 4.3 حماية HTML/CSS/JS من النسخ
```html
<!-- إضافة في <head> -->
<meta name="robots" content="noarchive">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">

<!-- إضافة Content Security Policy -->
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; 
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               frame-ancestors 'none';
               base-uri 'self';">
```

### 4.4 تشويش الكود JavaScript
```bash
# استخدام أدوات obfuscation
npm install -g javascript-obfuscator

javascript-obfuscator static/js/main.js --output static/js/main.min.js \
    --compact true \
    --controlFlowFlattening true \
    --deadCodeInjection true \
    --stringArray true \
    --rotateStringArray true \
    --selfDefending true
```

---

## 🔒 5. أفضل الممارسات الأمنية (Best Security Practices)

### 5.1 مراجعة دورية
```yaml
📅 جدول المراجعة الأمنية:
  أسبوعياً:
    - مراجعة Log Files للأنشطة المشبوهة
    - فحص محاولات الدخول الفاشلة
    - التحقق من سلامة النسخ الاحتياطية
  
  شهرياً:
    - تحديث المكتبات والإطارات (Dependencies)
    - فحص الثغرات الأمنية (Vulnerability Scan)
    - مراجعة صلاحيات المستخدمين
  
  ربع سنوي:
    - اختبار اختراق (Penetration Testing)
    - مراجعة سياسات الأمان
    - تدريب الفريق على الأمن السيبراني
```

### 5.2 النسخ الاحتياطي
```bash
# سكريبت للنسخ الاحتياطي اليومي
#!/bin/bash

# Backup Database
pg_dump $DATABASE_URL > /backups/db_$(date +%Y%m%d).sql

# Backup Supabase Storage
supabase storage download --bucket documents --output /backups/storage_$(date +%Y%m%d)

# Encrypt backup
gpg --symmetric --cipher-algo AES256 /backups/db_$(date +%Y%m%d).sql

# Upload to secure location (AWS S3 with encryption)
aws s3 cp /backups/ s3://raha-backups/ --recursive --sse AES256

# Delete old backups (keep last 30 days)
find /backups/ -mtime +30 -delete
```

### 5.3 مراقبة الأمان
```python
# Security Monitoring & Alerts
import logging
from datetime import datetime

class SecurityMonitor:
    def __init__(self):
        self.logger = logging.getLogger('security')
        
    def log_suspicious_activity(self, activity_type, details):
        """تسجيل النشاط المشبوه"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'type': activity_type,
            'details': details,
            'ip': request.remote_addr,
            'user_agent': request.headers.get('User-Agent')
        }
        
        self.logger.warning(f"Suspicious Activity: {log_entry}")
        
        # إرسال تنبيه إذا كان خطير
        if activity_type in ['brute_force', 'sql_injection', 'xss_attempt']:
            self.send_alert_email(log_entry)
            
    def send_alert_email(self, log_entry):
        """إرسال تنبيه بالبريد الإلكتروني"""
        # إرسال بريد للمسؤول
        pass
```

---

## 🌐 6. إعدادات Caddy المتقدمة للأمان

```caddyfile
# Caddyfile مع إعدادات الأمان المحسّنة

rahamedical.com, www.rahamedical.com {
    # Auto HTTPS with Let's Encrypt
    tls {
        protocols tls1.3
        ciphers TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    }
    
    # Security Headers
    header {
        # منع embedding في iframes من مواقع أخرى
        X-Frame-Options "DENY"
        
        # منع MIME type sniffing
        X-Content-Type-Options "nosniff"
        
        # تفعيل XSS Protection
        X-XSS-Protection "1; mode=block"
        
        # Referrer Policy
        Referrer-Policy "strict-origin-when-cross-origin"
        
        # Content Security Policy
        Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';"
        
        # HSTS (HTTP Strict Transport Security)
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        
        # Permissions Policy
        Permissions-Policy "geolocation=(), microphone=(), camera=()"
        
        # إزالة معلومات الخادم
        -Server
        -X-Powered-By
    }
    
    # Rate Limiting (requires Caddy plugin)
    rate_limit {
        zone dynamic {
            key {remote_host}
            events 100
            window 1m
        }
    }
    
    # Reverse Proxy to Backend
    reverse_proxy localhost:5000 {
        # Health check
        health_uri /health
        health_interval 30s
        health_timeout 5s
    }
    
    # تسجيل الأخطاء
    log {
        output file /var/log/caddy/access.log
        format json
        level ERROR
    }
}

api.rahamedical.com {
    tls {
        protocols tls1.3
    }
    
    # نفس Security Headers + إضافات للAPI
    header {
        X-Frame-Options "DENY"
        X-Content-Type-Options "nosniff"
        Access-Control-Allow-Origin "https://rahamedical.com"
        Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS"
        Access-Control-Allow-Headers "Content-Type, Authorization"
        Access-Control-Max-Age "86400"
    }
    
    reverse_proxy localhost:5000
}
```

---

## 📋 7. قائمة التحقق النهائية (Security Checklist)

### قبل الإطلاق:
- [ ] تأكد من أن `.env` غير موجود في Git
- [ ] تأكد من أن جميع API Keys سرية
- [ ] فعّل HTTPS على جميع النطاقات
- [ ] فعّل Row Level Security في Supabase
- [ ] راجع جميع الـ Headers الأمنية
- [ ] اختبر Rate Limiting
- [ ] فعّل النسخ الاحتياطي التلقائي
- [ ] أضف Monitoring و Logging
- [ ] اختبر جميع نماذج الإدخال ضد SQL Injection و XSS
- [ ] راجع صلاحيات المستخدمين
- [ ] أضف 2FA للحسابات الإدارية

### بعد الإطلاق:
- [ ] راقب Log Files يومياً
- [ ] حدّث Dependencies شهرياً
- [ ] أجرِ Penetration Testing ربع سنوي
- [ ] راجع النسخ الاحتياطية أسبوعياً
- [ ] راقب أداء الخادم والأمان

---

## ⚖️ 8. الاعتبارات القانونية والشفافية

### 8.1 الامتثال للقوانين
```yaml
القوانين المطبقة:
  - قانون حماية البيانات الهندي (DPDP Act 2023)
  - معايير HIPAA للسجلات الطبية
  - قوانين السياحة العلاجية الهندية
  - GDPR (للمستخدمين الأوروبيين إن وجد)

الإجراءات:
  ✅ سياسة خصوصية واضحة وشاملة
  ✅ شروط وأحكام محدثة (تم إزالة سياسة الاسترداد)
  ✅ نموذج موافقة واضح لجمع البيانات
  ✅ حق المستخدم في حذف بياناته
  ✅ شفافية في تقديرات التكاليف
```

### 8.2 بناء الثقة (Brain Equity & Subliminal Messaging)
```
⚠️ ملاحظة أخلاقية:
استخدام التلقين السري يجب أن يكون لبناء الثقة الحقيقية 
وليس للتلاعب بالعقول. نوصي بـ:

✅ استخدام تصميم نفسي إيجابي:
  - ألوان مريحة ومطمئنة (Teal/Green)
  - شهادات موثقة من مرضى حقيقيين
  - شفافية كاملة في المعلومات
  - عرض الاعتمادات الدولية بوضوح
  
✅ المحتوى النفسي الإيجابي:
  - قصص نجاح حقيقية
  - لغة مطمئنة وواضحة
  - توضيح المخاطر بجانب الفوائد
  - عدم المبالغة في الوعود

❌ تجنب:
  - الوعود الكاذبة
  - إخفاء المعلومات السلبية
  - التلاعب النفسي الضار
  - الضغط على المرضى
```

---

## 🚀 9. خطوات التنفيذ

### المرحلة 1: الأمان الأساسي (فوري)
```bash
1. فحص .gitignore
2. تفعيل HTTPS Headers في Caddy
3. تفعيل RLS في Supabase
4. إضافة Rate Limiting
```

### المرحلة 2: الحماية المتقدمة (خلال أسبوع)
```bash
1. إضافة copy protection و anti-screenshot
2. تشويش JavaScript
3. إضافة Watermarking
4. تفعيل Monitoring
```

### المرحلة 3: الأمان الشامل (خلال شهر)
```bash
1. اختبار اختراق شامل
2. تدقيق أمني كامل
3. إعداد خطة الاستجابة للحوادث
4. تدريب الفريق
```

---

## 📞 جهات الاتصال للطوارئ

```
🔴 في حالة اختراق أمني:
1. افصل الخادم فوراً
2. اتصل بفريق الطوارئ
3. احتفظ بـ Log Files
4. أبلغ المستخدمين المتأثرين
5. غيّر جميع كلمات المرور

📧 Emergency Contacts:
- Technical Lead: [email]
- Security Officer: [email]
- Hosting Provider: [provider support]
```

---

## 📚 موارد إضافية

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Supabase Security Best Practices](https://supabase.com/docs/guides/auth/row-level-security)
- [Caddy Security](https://caddyserver.com/docs/caddyfile/directives)
- [HIPAA Compliance Guide](https://www.hhs.gov/hipaa/index.html)
- [India DPDP Act 2023](https://www.meity.gov.in/writereaddata/files/Digital%20Personal%20Data%20Protection%20Act%202023.pdf)

---

**آخر تحديث:** ديسمبر 2024  
**المسؤول:** فريق Raha Medical التقني  
**مستوى السرية:** 🔴 سري للغاية - للاستخدام الداخلي فقط
