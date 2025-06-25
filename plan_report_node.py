"""
Plan Report Node

In this file is defined the node to create a plan for the report.
A plan means a detailed outline of the report, including the title and sections.

Author: L. Saetta
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from report_state import ReportState
from prompts import PROMPT_TEMPLATE_PLAN
from model_factory import get_chat_model
from utils import get_console_logger, extract_json_from_text
from config import DEBUG, DEFAULT_MAX_SECTIONS, DEFAULT_MIN_SECTIONS

logger = get_console_logger()


class PlanReportNode(Runnable):
    """
    Node to create a plan for the report
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Create a plan for the report
        """
        subject = state["subject"]
        report_length = state["report_length"]

        if report_length.lower() == "medium":
            # min, max # of sections in the report
            min_sections = 3
            max_sections = 5
        else:
            min_sections = DEFAULT_MIN_SECTIONS
            max_sections = DEFAULT_MAX_SECTIONS

        prompt_plan = PromptTemplate(
            input_variables=["subject", "min_sections", "max_sections"],
            template=PROMPT_TEMPLATE_PLAN,
        ).format(subject=subject, min_sections=min_sections, max_sections=max_sections)

        logger.info("Planning report...")

        # here we use the default model
        llm = get_chat_model()

        response = llm.invoke([HumanMessage(content=prompt_plan)])

        if DEBUG:
            logger.info("PlanReportNode: LLM output %s", response.content)

        try:
            parsed = extract_json_from_text(response.content)
        except Exception as e:
            logger.error("PlanReportNode: invalid JSON!")
            raise ValueError from e

        return {
            **state,
            "plan": parsed,
            "sections": parsed.get("sections", []),
            "current_section": 0,
            "section_drafts": [],
        }
