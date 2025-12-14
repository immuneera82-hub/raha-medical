# 🔧 إصلاح الأزرار والخريطة - دليل سريع

## ✅ ما تم إصلاحه (في الكود):

### 1. أزرار Hero Section
- ✅ زر "استشارة مجانية" → الآن يستخدم `onclick="showConsultationModal()"`
- ✅ زر "واتساب" أعلى الصفحة → الآن يستخدم `onclick="openWhatsApp()"`

---

## 📝 خطوات التنفيذ

### الخطوة 1: تحديث السيرفر
```bash
ssh root@srv941562
cd ~/raha-medical
git pull origin main
docker-compose restart backend
```

### الخطوة 2: إضافة Google Maps و WhatsApp في Supabase

افتح **Supabase SQL Editor** وشغّل هذا الكود:

```sql
-- 1. إضافة Google Maps URL
UPDATE hospitals 
SET google_maps_url = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3507.716980984494!2d77.08421631506014!3d28.431684182490744!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390d18c0f23ec663%3A0xf187aeba7fc5e7a1!2sArtemis%20Hospitals!5e0!3m2!1sen!2sin!4v1702377000000!5m2!1sen!2sin'
WHERE slug = 'artemis';

-- 2. إضافة رقم WhatsApp
UPDATE hospitals 
SET success_rates = jsonb_set(
  COALESCE(success_rates, '{}'::jsonb),
  '{contact}',
  '{
    "phone_india": "+911244511111",
    "phone_international": "+911244511111",
    "whatsapp": "911244511111",
    "email": "international@artemishospitals.com"
  }'::jsonb
)
WHERE slug = 'artemis';

-- 3. تحقق من النتيجة
SELECT 
  slug, 
  google_maps_url,
  success_rates->'contact'->>'whatsapp' as whatsapp
FROM hospitals 
WHERE slug = 'artemis';
```

---

## 🧪 اختبر النتائج

### بعد تشغيل SQL:

1. **افتح الصفحة:**
   ```
   https://rahamedical.com/hospitals/artemis
   ```

2. **اختبر الأزرار:**
   - ✅ اضغط "📞 استشارة مجانية" → يجب أن ينقلك لـ `/contact?hospital=artemis`
   - ✅ اضغط "💬 واتساب" → يجب أن يفتح WhatsApp مع رسالة مسبقة

3. **تحقق من الخريطة:**
   - ✅ انزل لقسم "الموقع والعنوان"
   - ✅ يجب أن ترى خريطة Google Maps تفاعلية

---

## 🎯 النتيجة المتوقعة

### قبل:
- ❌ الأزرار لا تعمل (href="#")
- ❌ الخريطة غير موجودة (placeholder)
- ❌ WhatsApp لا يفتح

### بعد:
- ✅ زر الاستشارة → يفتح صفحة Contact
- ✅ زر WhatsApp → يفتح محادثة مع رسالة مسبقة
- ✅ الخريطة → تظهر موقع المستشفى الحقيقي

---

## 💡 ملاحظة: رقم WhatsApp

الرقم الحالي: **+91 124 451 1111**

لتغييره لرقم آخر:
```sql
UPDATE hospitals 
SET success_rates = jsonb_set(
  success_rates,
  '{contact,whatsapp}',
  '"966XXXXXXXXX"'  -- ضع الرقم الصحيح هنا (بدون +)
)
WHERE slug = 'artemis';
```

---

## ✅ جاهز!
بعد تشغيل هذه الخطوات، كل شيء يجب أن يعمل بشكل كامل! 🚀
