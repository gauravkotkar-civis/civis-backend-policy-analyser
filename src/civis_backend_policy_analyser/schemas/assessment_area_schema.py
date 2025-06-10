from pydantic import Field
from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from typing import List, Optional
from datetime import datetime

class AssessmentAreaCreate(BaseModelSchema):
    assessment_name: Optional[str] = None
    description: Optional[str] = None
    created_by: Optional[str] = None
    prompt_ids: Optional[List[int]] = Field(default_factory=list)

class AssessmentAreaUpdate(BaseModelSchema):
    assessment_name: Optional[str] = None
    description: Optional[str] = None
    updated_by: Optional[str] = None
    prompt_ids: Optional[List[int]] = Field(default_factory=list)

class AssessmentAreaOut(BaseModelSchema):
    assessment_id: int
    assessment_name: str
    description: Optional[str]
    created_by: str
    created_on: Optional[datetime]
    updated_by: Optional[str]
    updated_on: Optional[datetime]
    prompt_ids: Optional[List[int]] = Field(default_factory=list)

    model_config = {
        "from_attributes": True
    }