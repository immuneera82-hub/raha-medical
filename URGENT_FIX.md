# 🚨 إصلاح عاجل - الأزرار والخريطة

## المشاكل المكتشفة:
1. ❌ صفحة /contact غير موجودة
2. ❌ الخريطة لا تظهر (لم يشغل SQL)
3. ❌ أزرار WhatsApp لا تعمل (السيرفر قديم)

---

## ✅ الحل الكامل (خطوة بخطوة):

### الخطوة 1: تحديث السيرفر
```bash
ssh root@srv941562
cd ~/raha-medical
git pull origin main
docker-compose restart backend
```

### الخطوة 2: تشغيل SQL في Supabase

**افتح Supabase Dashboard → SQL Editor → شغّل هذا:**

```sql
-- 1. إضافة Google Maps
UPDATE hospitals 
SET google_maps_url = 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3507.7169809844936!2d77.08421631506014!3d28.431684182490744!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x390d18c0f23ec663%3A0xf187aeba7fc5e7a1!2sArtemis%20Hospitals!5e0!3m2!1sen!2sin!4v1702377000000!5m2!1sen!2sin'
WHERE slug = 'artemis';

-- 2. إضافة contact info (WhatsApp + Phone)
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
```

### الخطوة 3: تحقق
```sql
SELECT 
  slug,
  google_maps_url IS NOT NULL as has_map,
  success_rates->'contact'->>'whatsapp' as whatsapp,
  success_rates->'contact'->>'phone_india' as phone
FROM hospitals 
WHERE slug = 'artemis';
```

**يجب أن ترى:**
- has_map: `true`
- whatsapp: `911244511111`
- phone: `+911244511111`

---

## 🧪 اختبار النتائج

بعد تنفيذ الخطوات أعلاه:

### 1. افتح الصفحة:
```
https://rahamedical.com/hospitals/artemis
```

### 2. اختبر:
- ✅ **زر "استشارة مجانية"** → يفتح WhatsApp
- ✅ **زر "واتساب"** أعلى الصفحة → يفتح WhatsApp
- ✅ **الخريطة** في قسم "الموقع والعنوان" → تظهر

---

## 💡 ملاحظات مهمة:

### رقم WhatsApp الحالي:
```
+91 124 451 1111 (Artemis Hospital الفعلي)
```

### لتغيير الرقم:
```sql
UPDATE hospitals 
SET success_rates = jsonb_set(
  success_rates,
  '{contact,whatsapp}',
  '"966XXXXXXXXX"'  -- ضع رقمك هنا
)
WHERE slug = 'artemis';
```

---

## ✅ النتيجة النهائية:

**قبل:**
- ❌ زر الاستشارة → "Not found"
- ❌ زر واتساب → لا يعمل
- ❌ الخريطة → placeholder

**بعد:**
- ✅ زر الاستشارة → WhatsApp مع رسالة "حجز استشارة"
- ✅ زر واتساب → WhatsApp مع رسالة "استفسار"
- ✅ الخريطة → موقع حقيقي تفاعلي

---

## 🚀 جاهز!
شغّل الخطوات أعلاه وأخبرني بالنتيجة!
