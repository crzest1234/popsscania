from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, Any

class AnalysisCreate(BaseModel):
    source_url: Optional[HttpUrl] = None

class AnalysisRead(BaseModel):
    id: int
    source_url: Optional[str]
    status: str
    metadata: Dict[str, Any]
    ml_result: Dict[str, Any]
    estimated_works: Dict[str, Any]
    rentability: Dict[str, Any]
    pdf_path: Optional[str]

    class Config:
        orm_mode = True
