
from fastapi import FastAPI, Request, Query, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse, JSONResponse
from pathlib import Path
import httpx
import io
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="Raha Medical API")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "static" / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

WATERMARK_LOGO_PATH = STATIC_DIR / "images" / "Raha-Medical-Favicon.png"

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/treatments", response_class=HTMLResponse)
async def treatments(request: Request):
    return templates.TemplateResponse("treatments.html", {"request": request})

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy-policy.html", {"request": request})

@app.get("/terms", response_class=HTMLResponse)
async def terms_and_conditions(request: Request):
    return templates.TemplateResponse("terms.html", {"request": request})

@app.get("/faq", response_class=HTMLResponse)
async def faq_page(request: Request):
    return templates.TemplateResponse("faq.html", {"request": request})

@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Raha Medical API"}


# Medical Report Processing API
@app.post("/api/process-report")
async def process_medical_report(
    file: UploadFile = File(...),
    patient_code: str = Form(...)
):
    """
    Process a medical report file and identify the test type.
    Returns the suggested filename based on content analysis.
    """
    try:
        from report_processor import process_report
        
        # Read file content
        file_bytes = await file.read()
        
        # Process the report
        result = process_report(file_bytes, file.filename, patient_code)
        
        return JSONResponse(content=result)
    
    except ImportError:
        # Fallback if OCR libraries not available
        from medical_keywords import extract_test_name, generate_report_name, get_file_extension
        
        extension = get_file_extension(file.filename)
        # Use default naming without OCR
        new_name = generate_report_name("Medical Report", patient_code, extension)
        
        return JSONResponse(content={
            'original_name': file.filename,
            'new_name': new_name,
            'test_type': 'Medical Report',
            'success': True,
            'note': 'OCR not available, using default name'
        })
    
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={'error': str(e), 'success': False}
        )


@app.post("/api/get-report-name")
async def get_report_name(
    filename: str = Form(...),
    patient_code: str = Form(...),
    test_type: str = Form(None)
):
    """
    Generate a standardized report name.
    If test_type is not provided, uses 'Medical Report' as default.
    """
    from medical_keywords import generate_report_name, get_file_extension
    
    extension = get_file_extension(filename)
    report_type = test_type if test_type else "Medical Report"
    new_name = generate_report_name(report_type, patient_code, extension)
    
    return {"new_name": new_name, "test_type": report_type}

# Import and Register Routers
from backend.routers import knowledge_base
app.include_router(knowledge_base.router)
