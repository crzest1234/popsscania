import os
from celery import Celery
from .ml_stub import analyze_images_stub
from .pdfgen import generate_pdf
from .config import settings
from .db import SessionLocal
from . import crud, models
from sqlalchemy.orm import Session

celery = Celery(__name__, broker=settings.REDIS_URL, backend=settings.REDIS_URL)

@celery.task()
def process_analysis(analysis_id: int, image_paths: list, source_url: str):
    # ML analysis (stub)
    ml = analyze_images_stub(image_paths)

    # Estimate works (simple heuristic)
    base = 5000
    factor = 1
    if ml["defects"]["humidity"]: factor += 0.6
    if ml["defects"]["cracks"]: factor += 0.4
    if ml["defects"]["old_kitchen"]: factor += 0.7
    estimated_min = int(base * factor)
    estimated_max = int(estimated_min * 1.6)
    estimated = {"min": estimated_min, "max": estimated_max}

    # Rentability heuristics (stub)
    estimated_rent = 800
    gross_yield = round((estimated_rent * 12) / (200000) * 100, 2)
    net_yield = round(gross_yield * 0.75, 2)
    rent = {"estimated_rent": estimated_rent, "gross_yield": gross_yield, "net_yield": net_yield}

    # Generate PDF
    out_dir = "/tmp"
    out_path = os.path.join(out_dir, f"report_{analysis_id}.pdf")
    analysis_meta = {"source_url": source_url, "created_at": ""}
    generate_pdf(analysis_meta, ml, estimated, rent, out_path)

    # Update DB
    db: Session = SessionLocal()
    try:
        crud.update_analysis_ml(db, analysis_id, ml, estimated, rent, pdf_path=out_path)
    finally:
        db.close()
    return {"status":"ok","analysis_id":analysis_id}
