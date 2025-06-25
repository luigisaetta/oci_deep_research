"""
Assemble Report Node

Author: L. Saetta
"""

from langchain_core.runnables import Runnable
from report_state import ReportState
from utils import get_console_logger

logger = get_console_logger(name="AssembleReportNode")


class AssembleReportNode(Runnable):
    """
    Assemble the report
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Assemble the report
        """
        logger.info("Assembling report...")

        title = state["plan"].get("title", "Untitled Report")
        full_text = f"# {title}\n\n"

        for section in state["section_drafts"]:
            full_text += section + "\n\n"

        state["full_report"] = full_text

        return state
