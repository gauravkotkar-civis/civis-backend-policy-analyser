from sqlalchemy import Column, Integer, String, Text, TIMESTAMP, func, Identity
from sqlalchemy.orm import Mapped, mapped_column, relationship
from civis_backend_policy_analyser.models.base import Base
from typing import List, Optional
from datetime import datetime

from civis_backend_policy_analyser.models.document_type_assessment_area import DocumentTypeAssessmentArea

class DocumentType(Base):
    __tablename__ = "document_type"

    doc_type_id = Column(Integer, primary_key=True, autoincrement=True)
    doc_type_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_by = Column(String(100))
    created_on = Column(TIMESTAMP, default=func.now())
    updated_by = Column(String(100))
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())

    assessment_areas = relationship( 
        "AssessmentArea",
        secondary=DocumentTypeAssessmentArea,
        back_populates="document_types"
    )

    @property
    def assessment_ids(self) -> list[int]:
        # Return list of IDs only if relationship is loaded
        if 'assessment_areas' not in self.__dict__:
            return []
        return [a.assessment_id for a in self.assessment_areas]
