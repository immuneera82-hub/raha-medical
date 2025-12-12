# تفعيل بيانات المستشفيات - دليل سريع

## المشكلة
```bash
docker exec raha-backend python -m backend.automation.seed_content
# Error: No such container: raha-backend
```

## الحل 1: إيجاد اسم الـ Container الصحيح

### الخطوة 1: عرض جميع الـ containers
```bash
docker ps -a
```

ابحث عن container يحتوي على `backend` أو `raha` أو `fastapi` في الاسم.

### الخطوة 2: بعد إيجاد الاسم الصحيح
```bash
# مثال: إذا كان الاسم raha-medical-backend-1
docker exec raha-medical-backend-1 python -m backend.automation.seed_content

# أو
docker exec <CONTAINER_NAME> python -m backend.automation.seed_content
```

---

## الحل 2: Supabase SQL Editor (موصى به للسرعة) ⚡

### الخطوة 1: افتح Supabase Dashboard
1. اذهب إلى: https://rusuwljflrremkszgstn.supabase.co
2. سجل دخول
3. اضغط على **SQL Editor** من القائمة الجانبية

### الخطوة 2: انسخ والصق هذا الكود SQL

```sql
-- 1. Artemis Hospital (Full Data with Quanta Chrome Laser)
INSERT INTO hospitals (
  slug, name_ar, name_en, city, location, image_url, 
  overview_ar, overview_en, is_partner, jci_accredited, success_rates
)
VALUES (
  'artemis',
  'مستشفيات أرتميس',
  'Artemis Hospitals',
  'غورغاون',
  'Sector 51, Gurugram, Haryana 122001, India',
  '/static/images/Artemis.png',
  '<p>تعد مستشفيات أرتميس (Artemis Hospitals) واحدة من أرقى المؤسسات الطبية في الهند، وهي أول مستشفى في مدينة غورغاون يحصل على اعتماد اللجنة المشتركة الدولية (JCI) واعتماد المستشفيات الوطنية (NABH).</p><p>تتميز أرتميس بتقديم رعاية طبية متكاملة عبر مختلف التخصصات، مع تركيز خاص على التكنولوجيا المتقدمة.</p>',
  'Artemis Hospitals is a state-of-the-art multi-specialty hospital in Gurgaon, India.',
  true,
  true,
  '{
    "technologies": [
      {"title": "Quanta Chrome Laser", "description": "أحدث تقنية ليزر Q-Switched في شمال الهند. جهاز متطور يوفر أكثر من 50 نوعاً من العلاجات الجلدية بما في ذلك علاج التصبغات، الكلف، آثار حب الشباب، وتوحيد لون البشرة."},
      {"title": "Da Vinci Robotic Surgery", "description": "نظام الجراحة الروبوتية الأكثر دقة للعمليات المعقدة."},
      {"title": "O-Arm Surgical Imaging", "description": "نظام تصوير متطور لزيادة الدقة أثناء جراحات العمود الفقري."}
    ],
    "news": [
      {"headline": "وصول جهاز Quanta Chrome Laser", "snippet": "أرتميس تعلن عن انفرادها بتوفير أحدث تكنولوجيا ليزر لتجديد البشرة في شمال الهند."},
      {"headline": "جائزة التميز في سلامة المرضى", "snippet": "حصل المستشفى على جائزة التميز الآسيوي لعام 2024."}
    ],
    "testimonials": [
      {"text": "تجربتي مع قسم الجلدية كانت ممتازة. جهاز الليزر الجديد أعطى نتيجة فورية للتصبغات.", "author": "أم عبد الله - العراق"},
      {"text": "المستشفى نظيف جداً والطاقم يتحدث العربية.", "author": "خالد - عمان"}
    ],
    "gallery": [
      "/static/images/artemis_tech_1.jpg",
      "/static/images/artemis_tech_2.jpg",
      "/static/images/artemis_tech_3.jpg"
    ]
  }'::jsonb
)
ON CONFLICT (slug) DO UPDATE SET
  name_ar = EXCLUDED.name_ar,
  overview_ar = EXCLUDED.overview_ar,
  success_rates = EXCLUDED.success_rates;

-- 2. Medanta
INSERT INTO hospitals (slug, name_ar, name_en, city, location, image_url, overview_ar, is_partner, jci_accredited)
VALUES ('medanta', 'مستشفى ميدانتا', 'Medanta - The Medicity', 'دلهي', 'Sector 38, Gurugram', '/static/images/Medanta.png', 'ميدانتا هي واحدة من أكبر المستشفيات متعددة التخصصات في الهند.', true, true)
ON CONFLICT (slug) DO UPDATE SET name_ar = EXCLUDED.name_ar;

-- 3. Fortis Healthcare
INSERT INTO hospitals (slug, name_ar, name_en, city, location, image_url, overview_ar, is_partner, jci_accredited)
VALUES ('fortis', 'مستشفيات فورتيس', 'Fortis Healthcare', 'مومباي', 'Mulund Goregaon Link Rd, Mumbai', '/static/images/Fortis.png', 'شبكة رعاية صحية رائدة في الهند، تشتهر بتميّزها في جراحات القلب والعظام.', true, true)
ON CONFLICT (slug) DO UPDATE SET name_ar = EXCLUDED.name_ar;

-- 4. Max Healthcare
INSERT INTO hospitals (slug, name_ar, name_en, city, location, image_url, overview_ar, is_partner, jci_accredited)
VALUES ('max-healthcare', 'ماكس هيلثكير', 'Max Healthcare', 'نيودلهي', 'Saket, New Delhi', '/static/images/Max-Healthcare.png', 'مجموعة مستشفيات ماكس تقدم رعاية طبية عالمية المستوى مع تركيز على علاج السرطان.', true, true)
ON CONFLICT (slug) DO UPDATE SET name_ar = EXCLUDED.name_ar;

-- 5. Marengo Asia
INSERT INTO hospitals (slug, name_ar, name_en, city, location, image_url, overview_ar, is_partner, jci_accredited)
VALUES ('marengo-asia', 'مارينغو آسيا', 'Marengo Asia Hospitals', 'غورغاون', 'Golf Course Ext Rd, Gurugram', '/static/images/Marengo-Asia.png', 'مستشفى حديث يركز على سلامة المرضى والتميز الإكلينيكي.', true, false)
ON CONFLICT (slug) DO UPDATE SET name_ar = EXCLUDED.name_ar;

-- 6. CK Birla
INSERT INTO hospitals (slug, name_ar, name_en, city, location, image_url, overview_ar, is_partner, jci_accredited)
VALUES ('ck-birla', 'مستشفيات سي كي بيرلا', 'CK Birla Hospitals', 'كولكاتا', 'Kolkata, West Bengal', '/static/images/CK-BIRLA.png', 'تشتهر بجودة الرعاية في مجال الخصوبة وصحة المرأة والقلب.', true, true)
ON CONFLICT (slug) DO UPDATE SET name_ar = EXCLUDED.name_ar;

-- Verify: Check all hospitals
SELECT slug, name_en, city, is_partner, jci_accredited 
FROM hospitals 
ORDER BY created_at DESC;
```

### الخطوة 3: اضغط "Run" أو Ctrl+Enter

ستظهر النتيجة في الأسفل تؤكد إضافة 6 مستشفيات.

---

## التحقق من النجاح

افتح المتصفح:
```
http://localhost:8000/
```

1. اذهب لقسم "المستشفيات العالمية المعتمدة"
2. يجب أن ترى 6 مستشفيات
3. اضغط على "أرتميس" للانتقال لصفحة التفاصيل
4. يجب أن ترى:
   - نبذة عن المستشفى
   - قسم "أحدث التقنيات" مع Quanta Chrome Laser
   - معرض الصور (3 صور)
   - آراء المرضى

---

## 🎯 الخلاصة

**الطريقة الموصى بها**: استخدم Supabase SQL Editor (الحل 2) ✅
- أسرع وأضمن
- لا يعتمد على Docker
- تظهر النتائج فوراً

**بعد التفعيل**:
- ✅ الصفحة الرئيسية تعرض المستشفيات
- ✅ Desktop: عرض ثابت أنيق
- ✅ Mobile: تمرير سلس لليمين
- ✅ صفحة Artemis تعمل: `/knowledge-base/hospital/artemis`
