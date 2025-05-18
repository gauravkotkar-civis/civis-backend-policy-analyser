import logging
import sys
import uvicorn

from contextlib import asynccontextmanager
from fastapi import FastAPI

from fastapi_project.core.db_connection import sessionmanager


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that handles startup and shutdown events.
    """
    yield
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, docs_url="/api/docs")


@app.get("/health-check")
async def root():
    return {"message": "Backend is running."}


# app.include_router()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8000)