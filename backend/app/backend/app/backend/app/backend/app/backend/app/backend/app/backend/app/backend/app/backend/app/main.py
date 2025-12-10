from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .db import get_db, Base, engine
from . import crud, schemas
from .tasks import process_analysis
import os
from typing import List
from .config import settings

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PropScan AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyses", response_model=schemas.AnalysisRead)
async def create_analysis(source_url: str = None, files: List[UploadFile] = File(default=None), db: Session = Depends(get_db)):
    # create analysis DB record
    a = crud.create_analysis(db, source_url=source_url)
    # store files to /tmp for stub - in prod upload to S3
    image_paths = []
    if files:
        for f in files:
            path = f"/tmp/{a.id}_{f.filename}"
            with open(path, "wb") as fh:
                fh.write(await f.read())
            image_paths.append(path)
    # launch Celery task
    process_analysis.delay(a.id, image_paths, source_url or "")
    return a

@app.get("/analyses/{analysis_id}", response_model=schemas.AnalysisRead)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    a = db.query(crud.models.Analysis).filter(crud.models.Analysis.id==analysis_id).first()
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    return a
