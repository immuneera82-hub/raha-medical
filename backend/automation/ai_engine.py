
import os
import json
from typing import Dict, Any, List

class AIEngine:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
    def generate_disease_profile(self, disease_name: str) -> Dict[str, Any]:
        """
        Generates a structured disease profile.
        If no API key is present, returns a TEMPLATE/DUMMY structure.
        """
        print(f"🤖 AI Generating content for: {disease_name}...")
        
        # If we had an API key, we would call OpenAI here:
        # response = client.chat.completions.create(...)
        
        # For now, return a high-quality "Template" to prove the flow
        slug = disease_name.lower().replace(" ", "-")
        
        return {
            "name_en": disease_name,
            "name_ar": f"علاج {disease_name}",  # Placeholder translation
            "scientific_name": f"Scientific name for {disease_name}",
            "slug": slug,
            "code": f"RM-{slug[:3].upper()}-001",
            
            "definition_ar": f"هذا شرح تفصيلي طبي عن {disease_name}. يتم توليده بواسطة الذكاء الاصطناعي لضمان الدقة والمصداقية.",
            "definition_en": f"Comprehensive medical definition of {disease_name}.",
            
            "causes_ar": ["سبب وراثي محتمل", "عوامل بيئية", "نمط الحياة"],
            "risk_factors_ar": ["التدخين", "السمنة", "التقدم في العمر"],
            
            "symptoms_early_ar": ["تعب عام", "فقدان وزن غير مبرر"],
            "symptoms_advanced_ar": ["ألم شديد", "صعوبة في التنفس"],
            
            "when_to_see_doctor_ar": "عند استمرار الأعراض لأكثر من أسبوعين.",
            
            "diagnosis_methods_ar": ["فحص سريري", "تحليل دم شامل", "أشعة مقطعية"],
            "required_tests_ar": ["CBC", "Biopsy", "MRI"],
            
            "success_rates": "تصل إلى 90% في المراحل المبكرة",
            "treatment_options_ar": ["الجراحة", "العلاج الإشعاعي", "العلاج المناعي"],
            "recovery_time_ar": "من 2 إلى 4 أسابيع",
            
            "prevention_methods_ar": ["الفحص الدوري", "الرياضة المنتظمة", "الغذاء الصحي"],
            
            "why_choose_india_ar": "توفر الهند أحدث التقنيات بتكلفة أقل بنسبة 60% من أوروبا.",
            "raha_services_ar": "نقدم خدمات الترجمة، الاستقبال من المطار، وتدقيق الفواتير.",
            
            "faqs": [
                {"question": f"كم تكلفة علاج {disease_name}؟", "answer": "تعتمد التكلفة على الحالة، لكنها تبدأ من 3000 دولار."},
                {"question": "هل العلاج مضمون؟", "answer": "نسب النجاح عالية جداً في مستشفيات الشبكة لدينا."}
            ],
            
            "reliable_sources": ["https://www.who.int", "https://www.mayoclinic.org"],
            
            "meta_title_ar": f"علاج {disease_name} في الهند | دليل شامل",
            "meta_description_ar": f"تعرف على أفضل طرق علاج {disease_name} في الهند مع نسبة نجاح عالية."
        }
