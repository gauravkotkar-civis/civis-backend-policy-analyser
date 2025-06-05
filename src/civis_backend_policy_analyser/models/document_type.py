from sqlalchemy.orm import Mapped, mapped_column

from civis_backend_policy_analyser.models.base import Base


class DocumentType(Base):
    __tablename__ = 'document_type'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    document_type_name: Mapped[str] = mapped_column(index=True, unique=True)

    def __repr__(self) -> str:
        return f'DocumentType(document_type_name={self.document_type_name})'
