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
