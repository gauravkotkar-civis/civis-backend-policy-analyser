from civis_backend_policy_analyser.models.base import Base
from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, func, UniqueConstraint, Identity
from sqlalchemy.orm import relationship

class DocumentTypeAssessmentArea(Base):
    __tablename__ = 'document_type_assessment_area'
    __table_args__ = (UniqueConstraint('doc_type_id', 'assessment_id', name='_doc_type_assessment_uc'),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    doc_type_id = Column(Integer, ForeignKey('document_type.doc_type_id', ondelete='CASCADE'), nullable=False)
    assessment_id = Column(Integer, ForeignKey('assessment_area.assessment_id', ondelete='CASCADE'), nullable=False)
    created_on = Column(TIMESTAMP, default=func.now())
    updated_on = Column(TIMESTAMP, default=func.now(), onupdate=func.now())



