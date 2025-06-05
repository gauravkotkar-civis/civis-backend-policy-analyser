from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class AssessmentAreaSchema(BaseModelSchema):
    id: int
    assessment_title: str
