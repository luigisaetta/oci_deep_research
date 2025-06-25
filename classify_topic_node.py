"""
Classify the topic, for reporting purpouse

Author: L. Saetta
"""

from langchain.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.messages import HumanMessage
from report_state import ReportState
from prompts import PROMPT_TEMPLATE_TOPIC
from model_factory import get_chat_model
from utils import get_console_logger, extract_json_from_text
from config import DEBUG

logger = get_console_logger(name="ClassifyTopicNode")


class ClassifyTopicNode(Runnable):
    """
    Node to create a plan for the report
    """

    def invoke(self, state: ReportState, config=None, **kwargs) -> ReportState:
        """
        Node to classify the topic
        """
        logger.info("Classifying topic...")

        subject = state["subject"]

        # templates are in prompts.py
        prompt_topic = PromptTemplate(
            input_variables=["subject"], template=PROMPT_TEMPLATE_TOPIC
        ).format(subject=subject)

        # here we use the default model
        llm = get_chat_model()

        try:
            response = llm.invoke([HumanMessage(content=prompt_topic)])

            if DEBUG:
                logger.info("ClassifyTopicNode: LLM output %s", response.content)

            json_result = extract_json_from_text(response.content)

            logger.info("Topic classified as: %s", json_result["topic"])
            logger.info("Report length classified as: %s", json_result["report_length"])

        except ValueError as e:
            logger.error("ClassifyTopicNode: error extracting JSON from LLM response!")
            raise ValueError(
                "ClassifyTopicNode: failed to extract JSON from LLM response"
            ) from e
        except Exception as e:
            logger.error("ClassifyTopicNode: generic error %s", e)
            raise ValueError from e

        return {
            **state,
            "topic": json_result["topic"],
            "report_length": json_result["report_length"],
        }
