from typing import List

from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema
from civis_backend_policy_analyser.schemas.assessment_area_schema import AssessmentAreaSchema


class DocumentTypeSchema(BaseModelSchema):
    id: int
    document_type_name: str

    # assessment_areas: List[AssessmentAreaSchema]

    class Config:
        orm_mode = True