from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


from civis_backend_policy_analyser.models.base import Base
from civis_backend_policy_analyser.models.document_type import DocumentType


class AssessmentArea(Base):
    __tablename__ = "assessment_area"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    assessment_title: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    document_type_id: Mapped[int] = mapped_column(
        ForeignKey("document_type.id"), index=True, nullable=False
    )
    

    # With this `document_type` object is accessible which has an association with the `assessment_area``
    document_type: Mapped[DocumentType] = relationship(
        "DocumentType",
        back_populates="assessment_areas"
    )

    def __repr__(self) -> str:
        return f"AssessmentArea(assessment_title={self.assessment_title})"
