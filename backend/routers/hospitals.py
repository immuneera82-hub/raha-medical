from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os
from pathlib import Path
from backend.database.client import get_supabase_client

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

# Templates
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "static" / "templates"))


@router.get("/", response_class=HTMLResponse)
async def hospitals_list(request: Request):
    """صفحة قائمة المستشفيات"""
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("hospitals").select("*").eq("is_partner", True).order("name_ar").execute()
        hospitals = response.data if response.data else []
    except Exception as e:
        print(f"Error fetching hospitals: {e}")
        hospitals = []
    
    return templates.TemplateResponse("hospitals/list.html", {
        "request": request,
        "hospitals": hospitals
    })


@router.get("/{slug}", response_class=HTMLResponse)
async def hospital_detail(request: Request, slug: str):
    """صفحة تفاصيل المستشفى"""
    supabase = get_supabase_client()
    
    try:
        # Fetch hospital data
        hosp_response = supabase.table("hospitals").select("*").eq("slug", slug).execute()
        
        if not hosp_response.data:
            raise HTTPException(status_code=404, detail="Hospital not found")
        
        hospital = hosp_response.data[0]
        
        # Fetch related doctors
        doc_response = supabase.table("doctors").select("*").eq("hospital_id", hospital['id']).limit(6).execute()
        doctors = doc_response.data if doc_response.data else []
        
        return templates.TemplateResponse("hospitals/detail.html", {
            "request": request,
            "hospital": hospital,
            "doctors": doctors
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching hospital {slug}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{slug}/specialties", response_class=HTMLResponse)
async def hospital_specialties(request: Request, slug: str):
    """صفحة تخصصات المستشفى"""
    supabase = get_supabase_client()
    
    try:
        # Fetch hospital data
        hosp_response = supabase.table("hospitals").select("*").eq("slug", slug).execute()
        
        if not hosp_response.data:
            raise HTTPException(status_code=404, detail="Hospital not found")
        
        hospital = hosp_response.data[0]
        
        # Extract specialties from 'success_rates' -> 'centers_of_excellence'
        specialties = []
        if hospital.get('success_rates') and hospital['success_rates'].get('centers_of_excellence'):
            specialties = hospital['success_rates']['centers_of_excellence']
            
        return templates.TemplateResponse("hospitals/specialties_list.html", {
            "request": request,
            "hospital": hospital,
            "specialties": specialties
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching hospital specialties {slug}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{slug}/specialties/{specialty_slug}", response_class=HTMLResponse)
async def hospital_specialty_detail(request: Request, slug: str, specialty_slug: str):
    """صفحة تفاصيل تخصص في مستشفى معين"""
    supabase = get_supabase_client()
    
    try:
        # Fetch hospital data
        hosp_response = supabase.table("hospitals").select("*").eq("slug", slug).execute()
        
        if not hosp_response.data:
            raise HTTPException(status_code=404, detail="Hospital not found")
        
        hospital = hosp_response.data[0]
        
        # 1. Fetch Global Specialty Info
        spec_response = supabase.table("specialties").select("*").eq("slug", specialty_slug).execute()
        global_specialty = spec_response.data[0] if spec_response.data else None
        
        # 2. Find Local Hospital Info for this specialty
        local_specialty = None
        if hospital.get('success_rates') and hospital['success_rates'].get('centers_of_excellence'):
            for center in hospital['success_rates']['centers_of_excellence']:
                # Loose matching if we don't have slugs in centers_of_excellence
                if global_specialty and (global_specialty['name_en'].lower() in center['name_en'].lower() or center['name_en'].lower() in global_specialty['name_en'].lower()):
                    local_specialty = center
                    break
                # Fallback: exact name match if slug didn't work (unlikely to have slug in param if not in DB)
                # If we assume specialty_slug passed in url matches a known specialty slug.
        
        return templates.TemplateResponse("hospitals/specialty_detail.html", {
            "request": request,
            "hospital": hospital,
            "global_specialty": global_specialty,
            "local_specialty": local_specialty,
            "specialty_slug": specialty_slug
        })
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching hospital specialty detail {slug}/{specialty_slug}: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
