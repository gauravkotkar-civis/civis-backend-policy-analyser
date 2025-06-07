from civis_backend_policy_analyser.models.prompt import Prompt
from civis_backend_policy_analyser.schemas.prompt_schema import PromptSchema
from civis_backend_policy_analyser.views.base_view import BaseView


class PromptView(BaseView):
    """
    This view controller manages access to the all type of Prompt.

    E.g.
        ```
        - policy prompt
        - consultation prompt
        - law prompt etc.
        ```
    """

    model = Prompt
    schema = PromptSchema
