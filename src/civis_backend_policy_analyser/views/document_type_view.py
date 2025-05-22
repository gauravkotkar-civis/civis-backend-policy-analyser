from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.document_type import DocumentType
from civis_backend_policy_analyser.schemas.document_type_schema import DocumentTypeSchema


class DocumentTypeView(BaseView):
    """
    This view controller manages access to the all type of documents.

    E.g.
        ```
        - policy document
        - consulation document
        - law document etc.
        ```
    """
    model = DocumentType
    schema = DocumentTypeSchema
