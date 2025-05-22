from typing import Any
from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseView:
    """
    Base Controller view manages all common or generic action required to handle request-response services.

    Particularly it manages initialization of routine activities for each service and other generic functionality.
    """
    model: Any = None
    schema: Any = None

    def __init__(self, db_session):
        self.db_session = db_session
        self.select = select(self.model)

    async def all(self):
        try:
            # 1 Fetch all records from the defined SqlAlchemy Model.
            all_records = (await self.db_session.execute(self.select)).scalars().all()

            # 2 Validate and serialize each record using pydanctic model.
            all_records = [self.schema.from_orm(model_obj) for model_obj in all_records]

            return all_records
        except:
            logger.error(f"Error while fetch all records from table : {self.model}.")
            raise

    async def filter(self, **filter_kw_args):
        try:
            # 1 Select the records based on the filter fields given in query param.
            result = (await self.db_session.execute(self.select.filter_by(**filter_kw_args))).scalars().all()

            # 2 Validate and serialize each record using pydanctic model.
            filter_records = [self.schema.from_orm(model_obj) for model_obj in result]

            return filter_records
        except:
            logger.error(f"Error while fetch records by filter id: {filter_kw_args} from table : {self.model}.")
            raise
