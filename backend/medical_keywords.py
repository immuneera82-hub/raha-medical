# Medical Report Keywords and Processing Service
# This module identifies medical test types from report content

import re
from typing import Optional, Tuple

# Medical keywords dictionary (English and Arabic)
MEDICAL_KEYWORDS = {
    # Blood Tests
    "CBC": ["cbc", "complete blood count", "تحليل الدم الشامل", "صورة الدم", "blood count", "hemoglobin", "هيموجلوبين", "wbc", "rbc", "platelets"],
    "Lipid Profile": ["lipid", "cholesterol", "كوليسترول", "دهون", "triglycerides", "hdl", "ldl", "الدهون الثلاثية"],
    "Liver Function": ["liver function", "alt", "ast", "وظائف الكبد", "bilirubin", "البيليروبين", "sgot", "sgpt", "alkaline phosphatase"],
    "Kidney Function": ["kidney", "creatinine", "كرياتينين", "وظائف الكلى", "urea", "يوريا", "bun", "gfr", "renal"],
    "Thyroid": ["thyroid", "tsh", "t3", "t4", "الغدة الدرقية", "ثايرويد"],
    "Blood Sugar": ["glucose", "blood sugar", "سكر الدم", "hba1c", "fasting glucose", "السكر التراكمي", "diabetes"],
    "Vitamin D": ["vitamin d", "فيتامين د", "25-oh", "d3", "d2"],
    "Vitamin B12": ["vitamin b12", "فيتامين ب12", "b12", "cobalamin"],
    "Iron Studies": ["iron", "ferritin", "حديد", "فيريتين", "tibc", "transferrin"],
    "Hormone Panel": ["hormone", "هرمون", "testosterone", "estrogen", "progesterone", "fsh", "lh", "prolactin"],
    "Tumor Markers": ["tumor marker", "cea", "afp", "ca125", "ca19-9", "psa", "دلالات الأورام"],
    "Urine Analysis": ["urine", "تحليل البول", "urinalysis", "urine culture"],
    "Stool Analysis": ["stool", "تحليل البراز", "fecal", "occult blood"],
    "HIV Test": ["hiv", "aids", "الإيدز"],
    "Hepatitis": ["hepatitis", "hbsag", "hcv", "التهاب الكبد", "hbv"],
    "Pregnancy Test": ["pregnancy", "hcg", "اختبار الحمل", "beta hcg"],
    "Allergy Test": ["allergy", "ige", "حساسية", "allergen"],
    "Coagulation": ["coagulation", "pt", "inr", "ptt", "تخثر الدم", "bleeding time"],
    
    # Imaging & Scans
    "X-Ray": ["x-ray", "xray", "أشعة سينية", "chest x-ray", "أشعة الصدر"],
    "CT Scan": ["ct scan", "ct", "computed tomography", "أشعة مقطعية", "cat scan"],
    "MRI Scan": ["mri", "magnetic resonance", "رنين مغناطيسي", "الرنين"],
    "Ultrasound": ["ultrasound", "sonography", "سونار", "موجات فوق صوتية", "echo", "doppler"],
    "Mammogram": ["mammogram", "mammography", "ماموجرام", "أشعة الثدي", "breast imaging"],
    "ECG": ["ecg", "ekg", "electrocardiogram", "تخطيط القلب", "رسم القلب"],
    "Echocardiogram": ["echocardiogram", "echo", "إيكو القلب", "cardiac echo"],
    "PET Scan": ["pet scan", "pet-ct", "positron emission"],
    "Bone Density": ["bone density", "dexa", "dxa", "هشاشة العظام", "osteoporosis"],
    "Endoscopy": ["endoscopy", "منظار", "gastroscopy", "colonoscopy", "منظار المعدة"],
    
    # Pathology
    "Biopsy": ["biopsy", "خزعة", "histopathology", "tissue sample"],
    "Pap Smear": ["pap smear", "مسحة عنق الرحم", "cervical cytology"],
    "Semen Analysis": ["semen", "sperm", "تحليل السائل المنوي", "sperm count"],
    
    # IVF Related
    "AMH Test": ["amh", "anti-mullerian", "مخزون المبيض"],
    "FSH Test": ["fsh", "follicle stimulating", "هرمون المنشط"],
    "Semen Analysis": ["semen analysis", "تحليل السائل المنوي", "sperm morphology", "sperm motility"],
    "Hysteroscopy": ["hysteroscopy", "منظار الرحم"],
    "HSG Test": ["hsg", "hysterosalpingography", "أشعة الصبغة", "صبغة الرحم"],
    
    # General
    "Medical Report": ["medical report", "تقرير طبي", "clinical report", "doctor report"],
    "Lab Report": ["lab report", "laboratory", "تقرير مختبر", "lab results"],
    "Prescription": ["prescription", "روشتة", "وصفة طبية", "medication"],
}

# Default category if no keywords match
DEFAULT_CATEGORY = "Medical Document"


def extract_test_name(text: str) -> str:
    """
    Analyze text content and identify the medical test type.
    Returns the identified test/scan name.
    """
    if not text:
        return DEFAULT_CATEGORY
    
    text_lower = text.lower()
    
    # Count keyword matches for each category
    matches = {}
    for category, keywords in MEDICAL_KEYWORDS.items():
        count = 0
        for keyword in keywords:
            if keyword.lower() in text_lower:
                count += 1
        if count > 0:
            matches[category] = count
    
    # Return the category with most matches
    if matches:
        best_match = max(matches, key=matches.get)
        return best_match
    
    return DEFAULT_CATEGORY


def generate_report_name(test_name: str, patient_code: str, extension: str = "") -> str:
    """
    Generate the final report name in format: Test Name - Patient Code.extension
    """
    # Clean up the test name
    clean_name = test_name.replace("/", "-").replace("\\", "-")
    
    # Create the final name
    if extension:
        if not extension.startswith("."):
            extension = "." + extension
        return f"{clean_name} - {patient_code}{extension}"
    
    return f"{clean_name} - {patient_code}"


def get_file_extension(filename: str) -> str:
    """Extract file extension from filename."""
    if "." in filename:
        return filename.rsplit(".", 1)[-1].lower()
    return ""
