"""
Do a final review

Author: L. Saetta
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from report_state import ReportState
from prompts import PROMPT_TEMPLATE_REVIEW
from model_factory import get_chat_model
from utils import get_console_logger
from config import FINAL_REPORT_MAX_TOKENS

logger = get_console_logger(name="ReviewReportNode")


class ReviewReportNode(Runnable):
    """
    Review the entire content
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Review the entire content
        """
        logger.info("Reviewing report...")

        full_report = state["full_report"]

        prompt_review = PromptTemplate(
            input_variables=["full_report"],
            template=PROMPT_TEMPLATE_REVIEW,
        ).format(full_report=full_report)

        # max_tokens increased for the final report
        llm = get_chat_model(max_tokens=FINAL_REPORT_MAX_TOKENS)

        try:
            reviewed = llm.invoke([HumanMessage(content=prompt_review)])
        except Exception as e:
            logger.error("ReviewReportNode: error reviewing report: %s", e)
            raise ValueError("ReviewReportNode: failed to review report") from e

        state["reviewed_report"] = reviewed.content

        return state
