from civis_backend_policy_analyser.views.base_view import BaseView
from civis_backend_policy_analyser.models.assessment_area import AssessmentArea
from civis_backend_policy_analyser.schemas.assessment_area_schema import AssessmentAreaSchema


class AssessmentAreaView(BaseView):
    """
    This view controller manages access to the all type of documents.

    E.g.
        ```
        - policy document
        - consulation document
        - law document etc.
        ```
    """
    model = AssessmentArea
    schema = AssessmentAreaSchema
