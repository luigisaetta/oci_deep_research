"""
Generate Section Node

Author: L. Saetta
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from report_state import ReportState
from prompts import PROMPT_TEMPLATE_GENERATE
from model_factory import get_chat_model
from utils import get_console_logger

logger = get_console_logger()


class GenerateSectionNode(Runnable):
    """
    Generate the content for a section
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Generate the content for a section
        """
        section = state["sections"][state["current_section"]]["title"]
        retrieved_info = state["retrieved_info"]

        logger.info("Generating section: %s...", section)

        prompt_generate = PromptTemplate(
            input_variables=["section", "retrieved_info"],
            template=PROMPT_TEMPLATE_GENERATE,
        ).format(section=section, retrieved_info=retrieved_info)

        llm = get_chat_model()

        draft = llm.invoke([HumanMessage(content=prompt_generate)])

        state["section_drafts"].append(draft.content)

        # switch to next section
        state["current_section"] += 1

        logger.info("Completed section: %s", section)

        return state
