from sqlalchemy.orm import Mapped, mapped_column

from civis_backend_policy_analyser.models.base import Base


class AssessmentArea(Base):
    __tablename__ = 'assessment_area'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    assessment_title: Mapped[str] = mapped_column(
        index=True, unique=True, nullable=False
    )

    def __repr__(self) -> str:
        return f'AssessmentArea(assessment_title={self.assessment_title})'
