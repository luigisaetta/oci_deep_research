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

logger = get_console_logger(name="PlanReportNode")


class PlanReportNode(Runnable):
    """
    Node to create a plan for the report
    """

    def get_num_sections(self, report_length: str) -> tuple:
        """
        Get the number of sections based on the report length

        Args:
            report_length (str): The length of the report, e.g., "short", "medium", "long".
        Returns:
            tuple: A tuple containing the minimum and maximum number of sections.
        """
        if report_length.lower() == "medium":
            # min, max # of sections in the report
            min_sections = 3
            max_sections = 5
        elif report_length.lower() == "short":
            min_sections = 1
            max_sections = 2
        else:
            min_sections = DEFAULT_MIN_SECTIONS
            max_sections = DEFAULT_MAX_SECTIONS

        return min_sections, max_sections

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Create a plan for the report
        """
        logger.info("Planning report...")

        subject = state["subject"]
        report_length = state["report_length"]

        min_sections, max_sections = self.get_num_sections(report_length)

        prompt_plan = PromptTemplate(
            input_variables=["subject", "min_sections", "max_sections"],
            template=PROMPT_TEMPLATE_PLAN,
        ).format(subject=subject, min_sections=min_sections, max_sections=max_sections)

        # here we use the default model
        llm = get_chat_model()

        try:
            response = llm.invoke([HumanMessage(content=prompt_plan)])

            if DEBUG:
                logger.info("PlanReportNode: LLM output %s", response.content)

            parsed = extract_json_from_text(response.content)
        except ValueError as e:
            logger.error("PlanReportNode: error extracting JSON from LLM response!")
            raise ValueError(
                "PlanReportNode: failed to extract JSON from LLM response"
            ) from e
        except Exception as e:
            logger.error("PlanReportNode: generic error %s", e)
            raise ValueError from e

        return {
            **state,
            "plan": parsed,
            "sections": parsed.get("sections", []),
            "current_section": 0,
            "section_drafts": [],
        }
