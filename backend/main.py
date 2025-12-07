cat > backend/main.py << 'ENDOFFILE'
from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
from pathlib import Path
import httpx
import io

from PIL import Image
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

app = FastAPI(title="Raha Medical API")

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "static" / "templates"

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

WATERMARK_LOGO_PATH = STATIC_DIR / "images" / "favicon.png"


def add_watermark_to_image(image_bytes: bytes, opacity: float = 0.12) -> bytes:
    try:
        original = Image.open(io.BytesIO(image_bytes)).convert("RGBA")
        
        if not WATERMARK_LOGO_PATH.exists():
            return image_bytes
        
        watermark = Image.open(WATERMARK_LOGO_PATH).convert("RGBA")
        
        wm_width = int(original.width * 0.15)
        wm_ratio = wm_width / watermark.width
        wm_height = int(watermark.height * wm_ratio)
        watermark = watermark.resize((wm_width, wm_height), Image.Resampling.LANCZOS)
        
        watermark_with_opacity = Image.new("RGBA", watermark.size, (0, 0, 0, 0))
        for x in range(watermark.width):
            for y in range(watermark.height):
                r, g, b, a = watermark.getpixel((x, y))
                watermark_with_opacity.putpixel((x, y), (r, g, b, int(a * opacity)))
        
        position = (original.width - wm_width - 20, original.height - wm_height - 20)
        
        output = Image.new("RGBA", original.size, (255, 255, 255, 255))
        output.paste(original, (0, 0))
        output.paste(watermark_with_opacity, position, watermark_with_opacity)
        
        final = output.convert("RGB")
        buffer = io.BytesIO()
        final.save(buffer, format="JPEG", quality=95)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error adding watermark to image: {e}")
        return image_bytes


def create_watermark_pdf_page(page_width: float, page_height: float, opacity: float = 0.08) -> io.BytesIO:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=(page_width, page_height))
    
    if WATERMARK_LOGO_PATH.exists():
        try:
            logo = ImageReader(str(WATERMARK_LOGO_PATH))
            
            logo_width = page_width * 0.12
            logo_height = logo_width
            
            x = (page_width - logo_width) / 2
            y = (page_height - logo_height) / 2
            
            c.saveState()
            c.setFillAlpha(opacity)
            c.drawImage(logo, x, y, width=logo_width, height=logo_height, mask='auto')
            c.restoreState()
        except Exception as e:
            print(f"Error creating watermark page: {e}")
    
    c.save()
    buffer.seek(0)
    return buffer


def add_watermark_to_pdf(pdf_bytes: bytes, opacity: float = 0.08) -> bytes:
    try:
        original_pdf = PdfReader(io.BytesIO(pdf_bytes))
        output_pdf = PdfWriter()
        
        for page in original_pdf.pages:
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            watermark_buffer = create_watermark_pdf_page(page_width, page_height, opacity)
            watermark_pdf = PdfReader(watermark_buffer)
            watermark_page = watermark_pdf.pages[0]
            
            page.merge_page(watermark_page)
            output_pdf.add_page(page)
        
        result_buffer = io.BytesIO()
        output_pdf.write(result_buffer)
        result_buffer.seek(0)
        return result_buffer.getvalue()
    except Exception as e:
        print(f"Error adding watermark to PDF: {e}")
        return pdf_bytes


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})


@app.get("/admin", response_class=HTMLResponse)
async def admin_panel(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})


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
ENDOFFILE