from sqlalchemy import select
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.assessment_area_schema import AssessmentAreaCreate, AssessmentAreaOut, AssessmentAreaUpdate
from civis_backend_policy_analyser.views.base_view import BaseView
import logging
from sqlalchemy.orm import selectinload

logger = logging.getLogger(__name__)


class AssessmentAreaView(BaseView):
    """
    This view controller manages access to the all type of assessment areas.

    E.g.
        ```
        - policy assessment area
        - consultation assessment area
        - law assessment area etc.
        ```
    """

    model = AssessmentArea
    schema = AssessmentAreaOut

    async def all_assessment_areas(self):
        all_records = (
            await self.db_session.execute(
                select(self.model).options(selectinload(self.model.prompts))
            )
        ).scalars().all()
        
        return [self.schema.from_orm(record) for record in all_records]

    async def create(self, data: AssessmentAreaCreate):
        prompt_ids = data.prompt_ids or []
        area_data = data.model_dump(exclude={'prompt_ids'})
        model_obj = self.model(**area_data)

        if prompt_ids:
            prompt_objs = (
                await self.db_session.execute(
                    select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
                )
            ).scalars().all()
            model_obj.prompts = prompt_objs

        self.db_session.add(model_obj)
        await self.db_session.commit()
        await self.db_session.refresh(model_obj)

        # Now returns AssessmentAreaOut with prompt_ids property correctly serialized
        return self.schema.from_orm(model_obj)

    async def update(self, id: int, data: AssessmentAreaUpdate):
        # Fetch with relationships loaded eagerly to avoid lazy-loading later
        result = await self.db_session.execute(
            select(self.model)
            .options(selectinload(self.model.prompts))
            .where(self.model.assessment_id == id)
        )
        model_obj = result.scalars().first()

        if not model_obj:
            raise ValueError(f"AssessmentArea with id {id} not found.")

        update_data = data.model_dump(exclude_unset=True)
        prompt_ids = update_data.pop("prompt_ids", None)

        # Update regular fields
        for key, value in update_data.items():
            setattr(model_obj, key, value)

        # Handle many-to-many relationship manually
        if prompt_ids is not None:
            # Fetch the Prompt objects for the provided IDs
            result = await self.db_session.execute(
                select(Prompt).where(Prompt.prompt_id.in_(prompt_ids))
            )
            prompt_objs = result.scalars().all()

            # Replace the relationship safely
            model_obj.prompts.clear()  # Remove old mappings
            model_obj.prompts.extend(prompt_objs)  # Add new mappings

        await self.db_session.commit()
        await self.db_session.refresh(model_obj)

        return self.schema.from_orm(model_obj)