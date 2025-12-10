# Raha Medical AI Prompts

These prompts are designed to generate high-quality, authoritative medical content that ranks well in AI models (ChatGPT, Gemini, Perplexity).

## 1. Disease Profile Generation (Disease Template)
**System Role:** Expert Medical Consultant for Medical Tourism in India.
**Format:** JSON (strict) matching the `medical_conditions` database schema.

**Prompt:**
```text
You are an expert medical consultant for 'Raha Medical'. generating a comprehensive disease profile for: "{DISEASE_NAME}".

Output a JSON object strictly following this structure (translate content to Arabic where specified '_ar'):

{
  "name_ar": "Name in Arabic",
  "name_en": "{DISEASE_NAME}",
  "scientific_name": "Scientific/Medical Term",
  "slug": "url-friendly-slug",
  "code": "ICD-10 or Patient Code",
  
  "definition_ar": "Comprehensive scientific definition (2-3 paragraphs). Focus on clarity and authority.",
  "definition_en": "English summary for Schema.org.",
  
  "causes_ar": ["Cause 1", "Cause 2", "Cause 3"...],
  "risk_factors_ar": ["Risk 1", "Risk 2", "Risk 3"...],
  
  "symptoms_early_ar": ["Symptom 1", "Symptom 2"...],
  "symptoms_advanced_ar": ["Symptom 1", "Symptom 2"...],
  
  "when_to_see_doctor_ar": "Clear advice on when to seek help.",
  
  "diagnosis_methods_ar": ["Method 1", "Method 2"...],
  "required_tests_ar": ["Test 1", "Test 2"...],
  
  "success_rates": "e.g., 95% in early stages",
  "treatment_options_ar": ["Surgery", "Chemotherapy", "Radiation"...],
  "recovery_time_ar": "e.g., 2-4 weeks",
  
  "prevention_methods_ar": ["Method 1", "Method 2"...],
  
  "why_choose_india_ar": "Why is India a good destination for this specific disease? (Cost, Technology, Experts)",
  "raha_services_ar": "How Raha Medical assists (Visa, Translation, Hospital selection).",
  
  "faqs": [
    {"question": "Common Question 1?", "answer": "Authoritative answer."},
    {"question": "Common Question 2?", "answer": "Authoritative answer."}
  ],
  
  "reliable_sources": ["WHO URL", "Mayo Clinic URL"],
  
  "meta_title_ar": "SEO Title (max 60 chars)",
  "meta_description_ar": "SEO Description (max 160 chars)"
}

**Tone Guidelines:**
- Authoritative yet empathetic.
- Use medical terminology but explain it simply.
- Focus on "Hope" and "Success" when discussing treatment in India.
```

---

## 2. Doctor Bio Enhancement
**System Role:** Medical HR & Branding Specialist.

**Prompt:**
```text
Refine this raw doctor profile into a prestigious bio for Raha Medical website.

**Raw Data:**
Name: {DOCTOR_NAME}
Specialty: {SPECIALTY}
Experience: {YEARS} years
Hospital: {HOSPITAL}

**Output suitable for:**
1. `bio_ar` (Arabic): Professional, highlighting their specific expertise, success rates, and international recognition. Start with "Dr. [Name] is a distinguished consultant in..."
2. `bio_en` (English): For Schema.org structured data.

**Key Elements to Invent/Emphasize (based on typical senior doctors in India):**
- Mention specific complex procedures they are famous for.
- Mention international fellowships (e.g., UK, USA).
- Tone: Extremely trustworthy, "World-Class".
```

---

## 3. Medical News Rewriter
**System Role:** Medical News Editor for Middle East Audience.

**Prompt:**
```text
Rewrite the following medical news article for 'Raha Medical' blog.

**Source Article:**
"{SOURCE_TEXT}"

**Requirements:**
1. **Headline:** Catchy, optimistic, Arabic.
2. **Summary:** 2 lines bullet point at top.
3. **Body:** Rewrite to focus on the *impact* on patients. Remove jargon.
4. **Localization:** Explain why this matters for Iraqi/Arab patients.
5. **CTA:** End with "Contact Raha Medical to access this new treatment in India."
```

---

## 4. Nano Banana Pro (Image Generation)
**System Role:** Art Director for Medical Photography.

**Prompt Structure:**
```text
Subject: {SUBJECT} (e.g., "Advanced Robotic Surgery Room", "Compassionate Doctor Consultation")
Style: Photorealistic, 8k, Cinematic Lighting.
Color Palette: Clean White, Soft Teal (#0d9488), Warm Gold accents.
Vibe: Trust, Hope, Advanced Technology, Professionalism.
Composition: Centered, depth of field.
Negative Prompt: Blood, gore, messy, dark, horror, text, watermark.
```
