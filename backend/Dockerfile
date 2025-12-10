FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app


# 1. Install dependencies first (Cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-ara \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 2. Copy code into a 'backend' directory to preserve package structure
COPY . backend/

# 3. Set PYTHONPATH so 'import backend.routers' works
ENV PYTHONPATH=/app

EXPOSE 8000

# 4. Run uvicorn pointing to the module inside the package
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]