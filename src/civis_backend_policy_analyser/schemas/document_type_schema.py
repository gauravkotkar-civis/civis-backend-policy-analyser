from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import Optional
from datetime import datetime


class DocumentTypeSchema(BaseModelSchema):
    doc_type_id: Optional[int]  = None
    doc_type_name: str
    description: Optional[str]  = None
    created_by: str
    created_on: Optional[datetime]  = None
    updated_by: Optional[str]  = None
    updated_on: Optional[datetime]  = None

    class Config:
        orm_mode = True
