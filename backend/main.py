
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from pathlib import Path
import httpx
import io



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


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


<<<<<<< HEAD
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Raha Medical API"}
=======
@app.get("/api/download")
async def download_with_watermark(
    url: str = Query(..., description="File URL"),
    filename: str = Query("document", description="File name")
):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=60.0)
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="File not found")
            file_bytes = response.content
            content_type = response.headers.get("content-type", "")
        if "pdf" in content_type.lower() or filename.lower().endswith(".pdf"):
            watermarked = add_watermark_to_pdf(file_bytes, opacity=0.08)
            media_type = "application/pdf"
            final_filename = filename if filename.endswith(".pdf") else f"{filename}.pdf"
        elif any(ext in content_type.lower() for ext in ["image", "jpeg", "jpg", "png"]):
            watermarked = add_watermark_to_image(file_bytes, opacity=0.12)
            media_type = "image/jpeg"
            final_filename = filename if any(filename.endswith(ext) for ext in [".jpg", ".jpeg", ".png"]) else f"{filename}.jpg"
        else:
            watermarked = file_bytes
            media_type = content_type or "application/octet-stream"
            final_filename = filename
        return StreamingResponse(
            io.BytesIO(watermarked),
            media_type=media_type,
            headers={"Content-Disposition": f'attachment; filename="{final_filename}"'}
        )
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "Raha Medical API"}
EOF
>>>>>>> 2e039f2cbdda32693e242332868985e7b9f24bdb
