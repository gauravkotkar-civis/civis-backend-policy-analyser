from fastapi import APIRouter
from typing import List

from civis_backend_policy_analyser.views.document_type_view import DocumentTypeView
from civis_backend_policy_analyser.schemas.document_type_schema import DocumentTypeSchema
from civis_backend_policy_analyser.core.db_connection import DBSessionDep



document_type_router = APIRouter(
    prefix="/api/document_types",
    tags=["document_types"],
    responses={404: {"description": "Document Type Not found"}},
)

@document_type_router.get(
    "/",
    response_model=List[DocumentTypeSchema],
)
async def get_all_document_types(
    db_session: DBSessionDep,
):
    """
    Get all the document types in json format.
    """
    document_service = DocumentTypeView(db_session)
    document_types = await document_service.all()
    return document_types

@document_type_router.get(
    "/{document_type_id}",
    response_model=List[DocumentTypeSchema],
)
async def get_all_document_types(
    document_type_id: int,
    db_session: DBSessionDep,
):
    """
    Get all the document types in json format.
    """
    document_service = DocumentTypeView(db_session)
    document_types = await document_service.filter(id=document_type_id)
    return document_types
