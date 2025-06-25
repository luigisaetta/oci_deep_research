"""
Workflow:
Here we define the structure of the Graph.

The agent is based on LangGraph and is designed to generate a research report.
"""

from langgraph.graph import StateGraph, START, END
from report_state import ReportState
from classify_topic_node import ClassifyTopicNode
from plan_report_node import PlanReportNode
from retrieve_info_node import RetrieveInfoNode
from generate_section_node import GenerateSectionNode
from assemble_report_node import AssembleReportNode
from review_report_node import ReviewReportNode


# ---- Graph Construction ----


# this is for the conditional edge
def all_sections_written(state: ReportState) -> str:
    """
    Defines the logic for a conditional edge
    """
    # cycle on build section until all the sections have been processed
    # it is ok for sequential processing, if you want to switch to
    # parallel, you need to modify here.
    if state["current_section"] >= len(state["sections"]):
        # all sections worked
        return "assemble"

    return "next_section"


def create_workflow():
    """
    Create the graph
    """
    workflow = StateGraph(ReportState)
    workflow.add_node("classify_topic_node", ClassifyTopicNode())
    workflow.add_node("plan_node", PlanReportNode())
    workflow.add_node("search_node", RetrieveInfoNode())
    workflow.add_node("generate_node", GenerateSectionNode())
    workflow.add_node("assemble_node", AssembleReportNode())
    workflow.add_node("review_node", ReviewReportNode())

    workflow.add_edge(START, "classify_topic_node")
    workflow.add_edge("classify_topic_node", "plan_node")
    workflow.add_edge("plan_node", "search_node")
    # search_node and generate_node will work on current section
    workflow.add_edge("search_node", "generate_node")

    # sections of the report are not generated in parallel but sequentially
    # check if there are some more sections to work
    workflow.add_conditional_edges(
        "generate_node",
        all_sections_written,
        {"next_section": "search_node", "assemble": "assemble_node"},
    )

    workflow.add_edge("assemble_node", "review_node")
    workflow.add_edge("review_node", END)

    # ---- Build Graph and Save ----
    app = workflow.compile()

    return app
