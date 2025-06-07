from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import Optional
from datetime import datetime

class AssessmentAreaSchema(BaseModelSchema):
    assessment_id: Optional[int]  = None
    assessment_name: Optional[str]  = None
    description: Optional[str]  = None
    created_by: Optional[str]  = None
    created_on: Optional[datetime]  = None
    updated_by: Optional[str]  = None
    updated_on: Optional[datetime]  = None

    class Config:
        orm_mode = True
