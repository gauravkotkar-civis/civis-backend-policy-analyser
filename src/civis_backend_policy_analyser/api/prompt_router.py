from fastapi import APIRouter

from civis_backend_policy_analyser.core.db_connection import DBSessionDep
from civis_backend_policy_analyser.schemas.prompt_schema import PromptSchema
from civis_backend_policy_analyser.views.prompt_view import PromptView

prompt_router = APIRouter(
    prefix='/api/prompt',
    tags=['prompt'],
    responses={404: {'description': 'No prompt found.'}},
)


@prompt_router.get(
    '/',
    response_model=list[PromptSchema],
)
async def get_prompts(
    db_session: DBSessionDep,
):
    """
    Get all prompts in json format.
    """
    prompt_service = PromptView(db_session)
    prompts = await prompt_service.all()
    return prompts


@prompt_router.post(
    '/',
    response_model=PromptSchema,
    status_code=201,
)
async def create_prompt(
    prompt: PromptSchema,
    db_session: DBSessionDep,
):
    """
    Create a new prompt.
    """
    prompt_service = PromptView(db_session)
    created_prompt = await prompt_service.create(prompt)
    return created_prompt


@prompt_router.put(
    "/{prompt_id}",
    response_model=PromptSchema,
)
async def update_prompt(
    prompt_id: int,
    prompt: PromptSchema,
    db_session: DBSessionDep,
):
    """
    Update an existing prompt.
    """
    prompt_service = PromptView(db_session)
    updated_prompt = await prompt_service.update(
        prompt_id, prompt
    )
    return updated_prompt


@prompt_router.delete(
    "/{prompt_id}",
    status_code=204,
)
async def delete_prompt(
    prompt_id: int,
    db_session: DBSessionDep,
):
    """
    Delete a prompt.
    """
    prompt_service = PromptView(db_session)
    response = await prompt_service.delete(prompt_id)
    return response
