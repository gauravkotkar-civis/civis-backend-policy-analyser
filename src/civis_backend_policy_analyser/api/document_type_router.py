from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.document_type_schema import (
    DocumentTypeSchema,
)
from civis_backend_policy_analyser.views.document_type_view import DocumentTypeView

document_type_router = APIRouter(
    prefix='/api/document_types',
    tags=['document_types'],
    responses={404: {'description': 'Document Type Not found'}},
)


@document_type_router.get(
    '/',
    response_model=list[DocumentTypeSchema],
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
    '/{document_type_id}',
    response_model=list[DocumentTypeSchema],
)
async def get_document_type(
    document_type_id: int,
    db_session: DBSessionDep,
):
    """
    Get all the document types in json format.
    """
    document_service = DocumentTypeView(db_session)
    document_types = await document_service.filter(id=document_type_id)
    return document_types


@document_type_router.post(
    '/',
    response_model=DocumentTypeSchema,
)
async def create_assessment_area(
    assessment_area: DocumentTypeSchema,
    db_session: DBSessionDep,
):
    """
    Create a new assessment area.
    """
    document_service = DocumentTypeView(db_session)
    created_document_type = await document_service.create(assessment_area)
    return created_document_type


@document_type_router.put(
    '/{assessment_area_id}',
    response_model=DocumentTypeSchema,
)
async def update_assessment_area(
    assessment_area_id: int,
    assessment_area: DocumentTypeSchema,
    db_session: DBSessionDep,
):
    """
    Update an existing assessment area.
    """
    document_service = DocumentTypeView(db_session)
    updated_document_type = await document_service.update(
        assessment_area_id, assessment_area
    )
    return updated_document_type


@document_type_router.delete(
    '/{assessment_area_id}',
    response_model=dict,
)
async def delete_assessment_area(
    assessment_area_id: int,
    db_session: DBSessionDep,
):
    """
    Delete an assessment area.
    """
    document_service = DocumentTypeView(db_session)
    response = await document_service.delete(assessment_area_id)
    return response
