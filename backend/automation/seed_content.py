
import os
from backend.database.client import get_supabase_client
from dotenv import load_dotenv

# Load env vars
load_dotenv()

def seed_database():
    print("🚀 Starting Content Seeding...")
    supabase = get_supabase_client()
    
    # 1. SPECIALTIES
    specialties = [
        {
            "slug": "oncology",
            "name_ar": "علاج الأورام والسرطان",
            "name_en": "Oncology",
            "description_ar": "أحدث تقنيات علاج السرطان، العلاج المناعي، والجراحات الدقيقة.",
            "description_en": "Advanced cancer treatment including immunotherapy and precision surgery."
        },
        {
            "slug": "orthopedics",
            "name_ar": "جراحة العظام والمفاصل",
            "name_en": "Orthopedics",
            "description_ar": "استبدال المفاصل، الطب الرياضي، وعلاج الكسور المعقدة.",
            "description_en": "Joint replacement, sports medicine, and complex fracture treatment."
        },
        {
            "slug": "spine-surgery",
            "name_ar": "جراحة العمود الفقري",
            "name_en": "Spine Surgery",
            "description_ar": "جراحات الانزلاق الغضروفي، تقويم العمود الفقري، والجراحات طفيفة التوغل.",
            "description_en": "Herniated disc surgery, spinal deformity correction, and minimally invasive spine surgery."
        },
        {
            "slug": "ivf-fertility",
            "name_ar": "علاج العقم وأطفال الأنابيب",
            "name_en": "IVF & Fertility",
            "description_ar": "تقنيات الحقن المجهري الحديثة ونسب نجاح عالمية.",
            "description_en": "Advanced ICSI techniques and world-class success rates."
        }
    ]
    
    print("\n🔹 Upserting Specialties...")
    for spec in specialties:
        try:
            # Check if exists
            existing = supabase.table("specialties").select("id").eq("slug", spec["slug"]).execute()
            if not existing.data:
                res = supabase.table("specialties").insert(spec).execute()
                print(f"✅ Added: {spec['name_en']}")
            else:
                print(f"ℹ️  Exists: {spec['name_en']}")
        except Exception as e:
            print(f"❌ Error adding {spec['name_en']}: {e}")

    # Reload specialties to get IDs
    specs_db = supabase.table("specialties").select("id, slug").execute()
    spec_map = {item['slug']: item['id'] for item in specs_db.data}

    # 2. DISEASES (High Quality Content)
    diseases = [
        {
            "slug": "knee-replacement",
            "related_specialty_id": spec_map.get("orthopedics"),
            "name_en": "Knee Replacement Surgery",
            "name_ar": "عملية استبدال مفصل الركبة",
            "scientific_name": "Total Knee Arthroplasty (TKA)",
            "code": "ORTHO-KNEE-001",
            "definition_ar": "جراحة دقيقة تهدف إلى استبدال أسطح مفصل الركبة المتآكلة أو التالفة بأسطح صناعية متطورة لتقليل الألم واستعادة حركة الركبة الطبيعية.",
            "definition_en": "A surgical procedure to replace the weight-bearing surfaces of the knee joint to relieve pain and disability.",
            "causes_ar": ["فخشونة الركبة (Osteoarthritis)", "التهاب المفاصل الروماتويدي", "إصابات الركبة القديمة", "السمنة المفرطة"],
            "symptoms_early_ar": ["ألم أثناء المشي", "تصلب صباحي في الركبة"],
            "symptoms_advanced_ar": ["ألم مستمر حتى وقت الراحة", "تشوه في شكل الساق", "عدم القدرة على صعود السلالم"],
            "diagnosis_methods_ar": ["أشعة إكس (X-Ray)", "الرنين المغناطيسي (MRI)", "فحص سريري لمدى الحركة"],
            "success_rates": "أكثر من 95% وتستمر المفاصل الصناعية الحديثة لأكثر من 20 عاماً.",
            "treatment_options_ar": ["استبدال كلي للمفصل", "استبدال جزئي للمفصل", "جراحة الروبوت (Robotic Surgery)"],
            "recovery_time_ar": "المشي في نفس يوم العملية، العودة للحياة الطبيعية خلال 4-6 أسابيع.",
            "why_choose_india_ar": "تتميز الهند باستخدام الروبوتات الجراحية الحديثة (MAKO, Da Vinci) بتكلفة تقل 70% عن أوروبا والولايات المتحدة.",
            "raha_services_ar": "نوفر باقات شاملة تشمل العلاج الطبيعي المكثف بعد العملية لضمان أفضل النتائج.",
            "meta_title_ar": "عملية استبدال مفصل الركبة في الهند | التكلفة ونسب النجاح",
            "meta_description_ar": "أفضل مستشفيات الهند لجراحة استبدال الركبة باستخدام الروبوت. تعرف على التكلفة ومدة الشفاء مع رحا ميديكال."
        },
        {
            "slug": "scoliosis-correction",
            "related_specialty_id": spec_map.get("spine-surgery"),
            "name_en": "Scoliosis Correction",
            "name_ar": "جراحة تصحيح اعوجاج العمود الفقري (الجنف)",
            "scientific_name": "Scoliosis Correction Surgery",
            "code": "SPINE-SCOL-001",
            "definition_ar": "عملية جراحية لتعديل انحناء العمود الفقري غير الطبيعي، تهدف إلى منع تفاقم التشوه وتحسين شكل الجسم ووظائف الرئة.",
            "definition_en": "Surgery to correct abnormal curvature of the spine.",
            "causes_ar": ["عوامل وراثية", "عيوب خلقية منذ الولادة", "أمراض عصبية عضلية"],
            "symptoms_early_ar": ["عدم استواء في الكتفين", "بروز أحد لوحي الكتف"],
            "symptoms_advanced_ar": ["صعوبة في التنفس", "ألم مزمن في الظهر", "تأثر القلب والرئتين"],
            "diagnosis_methods_ar": ["أشعة (EOS Imaging) ثلاثية الأبعاد", "قياس زاوية كوب (Cobb Angle)"],
            "success_rates": "نسبة نجاح عالية جداً في تصحيح الانحناء ومنع تدهوره.",
            "treatment_options_ar": ["الدمج الفقري (Spinal Fusion)", "القضبان المغناطيسية (Growing Rods) للأطفال", "جراحة غير تداخلية (Minimally Invasive)"],
            "recovery_time_ar": "الإقامة في المستشفى 5-7 أيام، والعودة للمدرسة/العمل خلال 4 أسابيع.",
            "why_choose_india_ar": "جراحون متخصصون أجروا آلاف الحالات المعقدة للأطفال والبالغين بنسب أمان عالية جداً.",
            "raha_services_ar": "نساعد في ترتيبات السفر للمرافقين وتوفير سكن قريب من المستشفى لفترة النقاهة.",
            "meta_title_ar": "علاج اعوجاج العمود الفقري في الهند | أفضل الأطباء والتكلفة",
            "meta_description_ar": "جراحات تصحيح الجنف (Scoliosis) في الهند بأحدث التقنيات. استشر أطباء رحا ميديكال الآن."
        },
        {
            "slug": "ivf-icsi",
            "related_specialty_id": spec_map.get("ivf-fertility"),
            "name_en": "IVF & ICSI",
            "name_ar": "الحقن المجهري وأطفال الأنابيب",
            "scientific_name": "In Vitro Fertilization (IVF) / ICSI",
            "code": "IVF-GEN-001",
            "definition_ar": "عملية إخصاب البويضة بالحيوان المنوي خارج الجسم في مختبر متخصص، ثم إعادة زرع الأجنة في رحم الأم. تعد الحل الأمثل للعديد من مشاكل العقم.",
            "definition_en": "Assisted reproductive technology where an egg is fertilized by sperm in vitro.",
            "causes_ar": ["انسداد قنوات فالوب", "ضعف الحيوانات المنوية", "تكيس المبايض", "العقم غير مبرر السبب"],
            "symptoms_early_ar": ["تأخر الحمل لأكثر من سنة"],
            "symptoms_advanced_ar": ["تكرار فشل الحمل الطبيعي"],
            "diagnosis_methods_ar": ["تحليل مخزون المبيض (AMH)", "السونار المهبلي", "تحليل السائل المنوي"],
            "success_rates": "تصل إلى 60-70% في المراكز الهندية المتقدمة (أعلى من المعدل العالمي).",
            "treatment_options_ar": ["الحقن المجهري (ICSI)", "نقل الأجنة المجمدة (FET)", "فحص الأجنة وراثياً (PGD)"],
            "recovery_time_ar": "لا توجد فترة نقاهة طويلة، يمكن العودة للحياة الطبيعية في اليوم التالي.",
            "why_choose_india_ar": "تعتبر الهند عاصمة العالم لعلاج العقم بسبب الخبرة الهائلة والتكلفة المنافسة جداً.",
            "raha_services_ar": "الخصوصية التامة، وتوفير مترجمات إناث لراحة المريضة.",
            "meta_title_ar": "أفضل مراكز الحقن المجهري في الهند | نسب نجاح مضمونة",
            "meta_description_ar": "حققي حلم الأمومة مع رحا ميديكال. نربطك بأشهر أطباء العقم في الهند ونسب نجاح عالمية."
        },
                {
            "slug": "breast-cancer",
            "related_specialty_id": spec_map.get("oncology"),
            "name_en": "Breast Cancer",
            "name_ar": "سرطان الثدي",
            "scientific_name": "Breast Carcinoma",
            "code": "ONCO-BC-001",
            "definition_ar": "نمو غير طبيعي لخلايا أنسجة الثدي. يعتبر الكشف المبكر هو العامل الحاسم في الشفاء التام.",
            "definition_en": "Cancer that forms in the cells of the breasts.",
            "causes_ar": ["طفرات جينية (BRCA1, BRCA2)", "التقدم في العمر", "التاريخ العائلي"],
            "symptoms_early_ar": ["كتلة غير مؤلمة في الثدي", "تغير في شكل الحلمة"],
            "symptoms_advanced_ar": ["تغير لون الجلد", "تورم الغدد الليمفاوية تحت الإبط"],
            "diagnosis_methods_ar": ["الماموجرام", "الموجات الصوتية", "الخزعة (Biopsy)"],
            "success_rates": "تتجاوز 98% في حال الكشف المبكر.",
            "treatment_options_ar": ["الاستئصال الجراحي (Kills)", "العلاج الإشعاعي", "العلاج الهرموني والموجه"],
            "recovery_time_ar": "تختلف حسب نوع العلاج، من شهر إلى 6 أشهر.",
            "why_choose_india_ar": "مراكز متخصصة في الحفاظ على الثدي (Breast Conservation Surgery) بدلاً من الاستئصال الكامل.",
            "raha_services_ar": "دعم نفسي ومرافقات طبيات طوال فترة العلاج.",
            "meta_title_ar": "علاج سرطان الثدي في الهند | خيارات متقدمة للحفاظ على الثدي",
            "meta_description_ar": "أحدث بروتوكولات علاج سرطان الثدي في الهند. جراحات تجميلية وترميمية فورية بعد الاستئصال."
        }
    ]

    print("\n🔹 Upserting Diseases...")
    for disease in diseases:
        try:
            # Check if exists (by slug)
            existing = supabase.table("medical_conditions").select("id").eq("slug", disease["slug"]).execute()
            
            # Since user wants comprehensive content, we will UPSERT (update if exists)
            # But Supabase-py `upsert` needs explicit handling or `insert` with upsert option locally.
            # Using delete-then-insert is safer for this script to ensure clean state, 
            # OR just update if exists.
            
            if existing.data:
                print(f"🔄 Updating: {disease['name_en']}")
                supabase.table("medical_conditions").update(disease).eq("slug", disease["slug"]).execute()
            else:
                print(f"✅ Inserting: {disease['name_en']}")
                supabase.table("medical_conditions").insert(disease).execute()
        except Exception as e:
                print(f"❌ Error processing {disease['name_en']}: {e}")

    print("\n✨ Seeding Complete!")

if __name__ == "__main__":
    seed_database()
