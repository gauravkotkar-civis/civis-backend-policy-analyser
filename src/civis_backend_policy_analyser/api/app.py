import logging
import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from civis_backend_policy_analyser.api.assessment_area_router import (
    assessment_area_router,
)
from civis_backend_policy_analyser.api.document_type_router import document_type_router
from civis_backend_policy_analyser.core.db_connection import sessionmanager

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# sqlalchemy.url = postgresql+asyncpg://ffg:ffg_jpmc_civis@localhost:5432/civis


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url='/api/docs')


@app.get('/health-check')
async def root():
    return {'message': 'Backend is running.'}


app.include_router(document_type_router)
app.include_router(assessment_area_router)


if __name__ == '__main__':
    uvicorn.run(
        'civis_backend_policy_analyser.api.app:app',
        host='0.0.0.0',
        reload=True,
        port=8000,
    )
