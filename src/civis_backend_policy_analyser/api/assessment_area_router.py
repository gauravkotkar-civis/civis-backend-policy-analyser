from fastapi import APIRouter
from typing import List

from civis_backend_policy_analyser.views.assessment_area_view import AssessmentAreaView
from civis_backend_policy_analyser.schemas.assessment_area_schema import AssessmentAreaSchema,AssessmentAreaCreateSchema
from civis_backend_policy_analyser.core.db_connection import DBSessionDep


assessment_area_router = APIRouter(
    prefix="/api/assessment_areas",
    tags=["assessment_area"],
    responses={404: {"description": "No assessment area found."}},
)

@assessment_area_router.get(
    "/",
    response_model=list[AssessmentAreaSchema],
)
async def get_assessment_areas(
    db_session: DBSessionDep,
):
    """
    Get all assessment areas in json format.
    """
    assessment_area_service = AssessmentAreaView(db_session)
    assessment_areas = await assessment_area_service.all()
    return assessment_areas

@assessment_area_router.get(
    "/{document_type_id}",
    response_model=list[AssessmentAreaSchema],
)
async def get_all_assessment_areas_by_document_type_id(
    document_type_id: int,
    db_session: DBSessionDep,
):
    """
    Get all the document types in json format.
    """
    assessment_area_service = AssessmentAreaView(db_session)
    assessment_areas = await assessment_area_service.filter(document_type_id=document_type_id)
    return assessment_areas

@assessment_area_router.post(
    "/",
    response_model=AssessmentAreaSchema,
)
async def create_assessment_area(
    assessment_area: AssessmentAreaCreateSchema,
    db_session: DBSessionDep,
):
    """
    Create a new assessment area.
    """
    assessment_area_service = AssessmentAreaView(db_session)
    created_assessment_area = await assessment_area_service.create(assessment_area)
    return created_assessment_area

@assessment_area_router.put(
    "/{assessment_area_id}",
    response_model=AssessmentAreaSchema,
)
async def update_assessment_area(
    assessment_area_id: int,
    assessment_area: AssessmentAreaCreateSchema,
    db_session: DBSessionDep,
):
    """
    Update an existing assessment area.
    """
    assessment_area_service = AssessmentAreaView(db_session)
    updated_assessment_area = await assessment_area_service.update(assessment_area_id, assessment_area)
    return updated_assessment_area

@assessment_area_router.delete(
    "/{assessment_area_id}",
    response_model=dict,
)
async def delete_assessment_area(
    assessment_area_id: int,
    db_session: DBSessionDep,
):
    """
    Delete an assessment area.
    """
    assessment_area_service = AssessmentAreaView(db_session)
    response = await assessment_area_service.delete(assessment_area_id)
    return response

