from civis_backend_policy_analyser.schemas.base_model import BaseModelSchema


class DocumentTypeSchema(BaseModelSchema):
    id: int
    document_type_name: str

    class Config:
        orm_mode = True
