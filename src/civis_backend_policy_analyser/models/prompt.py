from civis_backend_policy_analyser.models.base import Base
from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Identity
from sqlalchemy.orm import relationship

class Prompt(Base):
    __tablename__ = 'prompt'

    prompt_id = Column(Integer, primary_key=True, autoincrement=True)
    criteria = Column(String(255), nullable=False)
    question = Column(Text, nullable=False)
    created_by = Column(String(100))
    created_on = Column(TIMESTAMP, default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())
