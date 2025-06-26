"""
Validate Request Node

Author: L. Saetta
"""

from langchain_core.runnables import Runnable
from langchain.prompts import PromptTemplate
from report_state import ReportState
from prompts import PROMPT_TEMPLATE_VALIDATE_REQUEST
from model_factory import get_chat_model
from utils import get_console_logger, extract_json_from_text
from config import DEBUG

logger = get_console_logger(name="ValidateRequestNode")


class ValidateRequest(Runnable):
    """
    Node to validate if the user request is clear enough to start structured research.
    It checks if the request is specific and clear enough to proceed without further clarification.
    If the request is not clear, it sets `clarification_needed` to True in the ReportState.
    If the request is clear, it sets `clarification_needed` to False.
    This node uses a chat model to analyze the user input and determine clarity.
    It uses a simple prompt that asks the model to respond with 'yes' or 'no'
    based on the clarity of the request.
    """

    def __init__(self):
        """
        Initialize the ValidateRequest node.
        It uses a chat model to analyze the user input.
        """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Check if the user request is clear enough to start structured research.
        """
        prompt = PromptTemplate(
            input_variables=["user_input"], template=PROMPT_TEMPLATE_VALIDATE_REQUEST
        ).format(user_input=state["subject"])

        if DEBUG:
            logger.debug("Validating request: %s", prompt)

        llm = get_chat_model()

        try:
            decision = llm.invoke(prompt).content

            json_result = extract_json_from_text(decision)

        except Exception as e:
            logger.error("ValidateRequestNode: error validating request: %s", e)
            raise ValueError("ValidateRequestNode: failed to validate request") from e

        if DEBUG:
            logger.debug("ValidateRequestNode: LLM decision: %s", decision)

        if json_result["decision"].lower() == "yes":
            state["clarification_needed"] = False
            state["clarification_request"] = None
        else:
            state["clarification_needed"] = True
            state["clarification_request"] = json_result.get(
                "clarification_request", ""
            )

        if state["clarification_needed"]:
            logger.info("Clarification needed: %s", state["clarification_request"])

        return state
