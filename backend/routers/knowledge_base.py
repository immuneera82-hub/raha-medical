
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from pathlib import Path
from backend.database.client import get_supabase_client

router = APIRouter(prefix="/knowledge-base", tags=["knowledge-base"])

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "static" / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/")
async def knowledge_base_hub(request: Request):
    """
    Main hub for Knowledge Base.
    Fetches top specialties and featured diseases.
    """
    supabase = get_supabase_client()
    
    # Fetch Specialties
    specialties_response = supabase.table("specialties").select("*").execute()
    specialties = specialties_response.data
    
    return templates.TemplateResponse("knowledge_base/index.html", {
        "request": request,
        "specialties": specialties
    })

@router.get("/disease/{slug}")
async def disease_detail(request: Request, slug: str):
    """
    Dynamic Disease Detail Page.
    Fetches all details for a medical condition.
    """
    supabase = get_supabase_client()
    
    # Fetch Condition Data
    response = supabase.table("medical_conditions").select("*, hospitals(*), related_specialty_id(*)").eq("slug", slug).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Disease not found")
        
    condition = response.data[0]
    
    return templates.TemplateResponse("knowledge_base/disease_detail.html", {
        "request": request,
        "condition": condition,
        "meta_title": condition.get('meta_title_ar', condition.get('name_ar')),
        "meta_description": condition.get('meta_description_ar', '')
    })

@router.get("/doctor/{slug}")
async def doctor_detail(request: Request, slug: str):
    """
    Dynamic Doctor Profile Page.
    """
    supabase = get_supabase_client()
    
    response = supabase.table("doctors").select("*, hospitals(*)").eq("slug", slug).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Doctor not found")
        
    doctor = response.data[0]
    
    return templates.TemplateResponse("knowledge_base/doctor_detail.html", {
        "request": request,
        "doctor": doctor
    })

@router.get("/hospitals")
async def hospitals_list(request: Request):
    """
    List of partner hospitals.
    """
    supabase = get_supabase_client()
    response = supabase.table("hospitals").select("*").eq("is_partner", True).execute()
    
    return templates.TemplateResponse("knowledge_base/hospitals_list.html", {
        "request": request,
        "hospitals": response.data
    })

@router.get("/hospital/{slug}")
async def hospital_detail_redirect(slug: str):
    """
    Redirect old hospital URLs to new location.
    """
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url=f"/hospitals/{slug}", status_code=301)

