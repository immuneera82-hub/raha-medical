# 🔧 إصلاح سريع - تحديث بيانات Artemis في Supabase

## المشكلة
الـ Internal Server Error يحدث لأن البيانات في `success_rates` غير موجودة أو غير كاملة.

## الحل السريع
افتح **Supabase SQL Editor** وشغّل هذا الأمر:

```sql
-- تحديث بيانات Artemis Hospital مع كل الحقول المطلوبة
UPDATE hospitals 
SET success_rates = '{
  "quick_facts": {
    "established_year": "2007",
    "total_beds": "380",
    "specialties_count": "40+",
    "languages": ["العربية", "الإنجليزية", "الهندية"],
    "arab_patients_yearly": "2500+",
    "success_rate_cardiology": "98%",
    "success_rate_oncology": "92%",
    "ivf_success_rate": "65%"
  },
  
  "certifications": [
    {
      "name": "JCI (Joint Commission International)",
      "year": "2013",
      "renewal": "2024",
      "description": "اعتماد دولي للجودة والسلامة في الرعاية الصحية"
    },
    {
      "name": "NABH",
      "year": "2010",
      "description": "الاعتماد الوطني الهندي للمستشفيات"
    },
    {
      "name": "ISO 9001:2015",
      "year": "2015",
      "description": "نظام إدارة الجودة الدولي"
    }
  ],
  
  "centers_of_excellence": [
    {
      "name_ar": "مركز علوم القلب والأوعية الدموية",
      "name_en": "Cardiac Sciences Center",
      "icon": "heart",
      "description": "12,000+ عملية قلب مفتوح ناجحة | نسبة نجاح 98%",
      "treatments": ["قسطرة القلب", "عملية القلب المفتوح", "جراحة الصمامات"]
    },
    {
      "name_ar": "مركز علاج الأورام والسرطان",
      "name_en": "Cancer Care Center",
      "icon": "ribbon",
      "description": "علاج شامل: كيميائي، إشعاعي، مناعي، وجراحي",
      "treatments": ["سرطان الثدي", "سرطان القولون", "سرطان الرئة"]
    }
  ],
  
  "technologies": [
    {
      "title": "Quanta Chrome Laser",
      "category": "dermatology",
      "description": "أحدث تقنية ليزر Q-Switched في شمال الهند",
      "benefits": ["علاج التصبغات والكلف", "إزالة آثار حب الشباب", "تفتيح البشرة"],
      "treatments_offered": "50+",
      "first_in": "North India",
      "image_url": "/static/images/artemis_quanta_laser.png"
    },
    {
      "title": "Da Vinci Xi Robotic Surgery",
      "category": "surgery",
      "description": "أحدث جيل من أنظمة الجراحة الروبوتية",
      "benefits": ["جراحات طفيفة التوغل", "نزيف أقل", "تعافي أسرع"],
      "used_in": ["جراحة المسالك البولية", "جراحة الأورام"],
      "image_url": "/static/images/artemis_surgery_room.png"
    }
  ],
  
  "news": [
    {
      "date": "2024-11-15",
      "headline": "مستشفى أرتميس يستقبل جهاز Quanta Chrome Laser",
      "snippet": "الأول في شمال الهند - يوفر أكثر من 50 علاج جلدي",
      "importance": "high",
      "category": "equipment"
    },
    {
      "date": "2024-09-10",
      "headline": "جائزة أفضل مستشفى متعدد التخصصات 2024",
      "snippet": "تقديراً للتميز في الرعاية الطبية",
      "importance": "medium",
      "category": "award"
    }
  ],
  
  "testimonials": [
    {
      "patient_name": "أحمد العلي",
      "country": "العراق",
      "treatment": "عملية قلب مفتوح",
      "rating": 5,
      "text": "تجربة ممتازة، الفريق الطبي محترف جداً",
      "date": "2024-11-01",
      "verified": true
    },
    {
      "patient_name": "فاطمة المنصور",
      "country": "السعودية",
      "treatment": "علاج سرطان الثدي",
      "rating": 5,
      "text": "د. سانديب باترا طبيب ماهر، النتائج ممتازة",
      "date": "2024-10-15",
      "verified": true
    }
  ],
  
  "arab_services": {
    "interpreters": true,
    "halal_food": true,
    "prayer_rooms": true,
    "airport_pickup": true,
    "visa_assistance": true,
    "24_7_arabic_support": true
  },
  
  "gallery": [
    "/static/images/artemis_exterior.png",
    "/static/images/artemis_quanta_laser.png",
    "/static/images/artemis_surgery_room.png",
    "/static/images/artemis_doctors_team.png"
  ]
}'::jsonb
WHERE slug = 'artemis';

-- تحقق من التحديث
SELECT slug, name_ar, success_rates->>'quick_facts' FROM hospitals WHERE slug = 'artemis';
```

---

## بعد تشغيل SQL

### 1. على السيرفر:
```bash
ssh root@srv941562
cd ~/raha-medical
git pull origin main
docker-compose down
docker-compose up -d --build
```

### 2. اختبر:
```
https://rahamedical.com/knowledge-base/hospital/artemis
```

---

## إذا استمرت المشكلة

تحقق من logs السيرفر:
```bash
docker logs -f raha-medical-backend-1 --tail 100
```

أو اختبر locally:
```bash
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

ثم افتح:
```
http://localhost:8000/knowledge-base/hospital/artemis
```
