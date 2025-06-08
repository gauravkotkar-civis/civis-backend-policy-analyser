from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class DocumentTypeCreate(BaseModel):
    doc_type_name: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    assessment_ids: Optional[List[int]] = []

class DocumentTypeUpdate(BaseModel):
    doc_type_name: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[str] = None
    assessment_ids: Optional[List[int]] = []

class DocumentTypeOut(BaseModel):
    doc_type_id: int
    doc_type_name: str
    description: Optional[str]
    created_by: str
    created_on: Optional[datetime]
    updated_by: Optional[str]
    updated_on: Optional[datetime]
    assessment_ids: Optional[List[int]] = []

    model_config = {
        "from_attributes": True
    }
