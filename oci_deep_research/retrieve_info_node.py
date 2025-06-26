"""
Retrieve Info Node

Author: L. Saetta
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from .report_state import ReportState
from .prompts import PROMPT_TEMPLATE_SEARCH
from .model_factory import get_chat_model
from .utils import get_console_logger
from .config import DEBUG, SEARCH_INFO_MODEL_ID

logger = get_console_logger(name="RetrieveInfoNode")


class RetrieveInfoNode(Runnable):
    """
    Retrieve info for creating a section of the report.

    This node uses a search model from OpenAI to gather information.
    It retrieves key points and summaries from credible sources
    about the current section of the report based on the subject.
    The retrieved information is stored in the state for later use
    in generating the section content.
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Retrieve info for creating a section of the report
        """
        section = state["sections"][state["current_section"]]["title"]

        logger.info("Retrieving info for %s...", section)

        llm = get_chat_model(model_id=SEARCH_INFO_MODEL_ID)

        # templates are in prompts.py
        prompt_search = PromptTemplate(
            input_variables=["section", "subject"], template=PROMPT_TEMPLATE_SEARCH
        ).format(section=section, subject=state["subject"])

        if DEBUG:
            logger.info("Retrieving info for: %s", prompt_search)

        try:
            info = llm.invoke([HumanMessage(content=prompt_search)])

            if DEBUG:
                logger.info("Info retrieved: %s", info.content)
        except Exception as e:
            logger.error("RetrieveInfoNode: error retrieving info: %s", e)
            raise ValueError("RetrieveInfoNode: failed to retrieve info") from e

        return {**state, "retrieved_info": info.content}
