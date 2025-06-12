from sqlalchemy import select
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.schemas.document_type_schema import (
    DocumentTypeCreate,
    DocumentTypeUpdate,
    DocumentTypeOut,
)
from civis_backend_policy_analyser.views.base_view import BaseView
import logging
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)


class DocumentTypeView(BaseView):
    """
    This view controller manages access to the all type of documents.

    E.g.
        ```
        - policy document
        - consulation document
        - law document etc.
        ```
    """

    model = DocumentType
    schema = DocumentTypeOut

    async def all_document_types(self):
        all_records = (
            await self.db_session.execute(
                select(self.model).options(selectinload(self.model.assessment_areas))
            )
        ).scalars().all()

        return [self.schema.from_orm(record) for record in all_records]

    async def create(self, data: DocumentTypeCreate):
        assessment_ids = data.assessment_ids or []
        doc_data = data.model_dump(exclude={'assessment_ids'})
        model_obj = self.model(**doc_data)

        if assessment_ids:
            assessment_objs = (
                await self.db_session.execute(
                    select(AssessmentArea).where(AssessmentArea.assessment_id.in_(assessment_ids))
                )
            ).scalars().all()
            model_obj.assessment_areas = assessment_objs

        self.db_session.add(model_obj)
        await self.db_session.commit()
        await self.db_session.refresh(model_obj)

        # Now returns DocumentTypeOut with assessment_ids property correctly serialized
        return self.schema.from_orm(model_obj)

    async def update(self, id: int, data: DocumentTypeUpdate):
        # Fetch with relationships loaded eagerly to avoid lazy-loading later
        result = await self.db_session.execute(
            select(self.model)
            .options(selectinload(self.model.assessment_areas))
            .where(self.model.doc_type_id == id)
        )
        model_obj = result.scalars().first()

        if not model_obj:
            raise ValueError(f"DocumentType with id {id} not found.")

        update_data = data.model_dump(exclude_unset=True)
        assessment_ids = update_data.pop("assessment_ids", None)

        # Update regular fields
        for key, value in update_data.items():
            setattr(model_obj, key, value)

        # Handle many-to-many relationship manually
        if assessment_ids is not None:
            # Fetch the AssessmentArea objects for the provided IDs
            result = await self.db_session.execute(
                select(AssessmentArea).where(AssessmentArea.assessment_id.in_(assessment_ids))
            )
            assessment_objs = result.scalars().all()

            # Replace the relationship safely
            model_obj.assessment_areas.clear()  # Remove old mappings
            model_obj.assessment_areas.extend(assessment_objs)  # Add new mappings

        await self.db_session.commit()
        await self.db_session.refresh(model_obj)

        return self.schema.from_orm(model_obj)