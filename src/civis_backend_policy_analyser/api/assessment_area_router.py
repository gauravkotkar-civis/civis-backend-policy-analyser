from fastapi import APIRouter
from typing import List

from civis_backend_policy_analyser.views.assessment_area_view import AssessmentAreaView
from civis_backend_policy_analyser.schemas.assessment_area_schema import AssessmentAreaSchema
from civis_backend_policy_analyser.core.db_connection import DBSessionDep


assessment_area_router = APIRouter(
    prefix="/api/assessment_areas",
    tags=["assessment_area"],
    responses={404: {"description": "No assessment area found."}},
)

@assessment_area_router.get(
    "/{document_type_id}",
    response_model=List[AssessmentAreaSchema],
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
