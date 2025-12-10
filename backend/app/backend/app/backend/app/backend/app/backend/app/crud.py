from sqlalchemy.orm import Session
from . import models, schemas
from typing import Optional

def create_analysis(db: Session, source_url: Optional[str]=None, user_id: Optional[int]=None):
    a = models.Analysis(user_id=user_id, source_url=source_url)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

def update_analysis_ml(db: Session, analysis_id: int, ml_result: dict, estimated_works: dict, rentability: dict, pdf_path: str):
    a = db.query(models.Analysis).filter(models.Analysis.id==analysis_id).first()
    if not a:
        return None
    a.ml_result = ml_result
    a.estimated_works = estimated_works
    a.rentability = rentability
    a.pdf_path = pdf_path
    a.status = "done"
    db.add(a)
    db.commit()
    db.refresh(a)
    return a
