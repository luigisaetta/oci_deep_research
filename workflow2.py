"""
Workflow2, with validate_request
"""

from langgraph.graph import StateGraph, START, END
from report_state import ReportState
from validate_request import ValidateRequest
from classify_topic_node import ClassifyTopicNode
from plan_report_node import PlanReportNode


def create_workflow():
    """
    Create the workflow graph with validation step.
    """
    workflow = StateGraph(ReportState)

    # Nodes
    workflow.add_node("validate_request", ValidateRequest())
    workflow.add_node("classify_topic_node", ClassifyTopicNode())
    workflow.add_node("plan_node", PlanReportNode())

    # Routing based on validation
    def route_on_validation(state: ReportState) -> str:
        """
        Route based on the validation result.
        If clarification is not needed, it routes to 'classify_topic_node'.
        """
        result = state.get("clarification_needed", False)

        return "classify_topic_node" if result is False else END

    # Entry point
    workflow.add_edge(START, "validate_request")

    # Add conditional transition
    workflow.add_conditional_edges("validate_request", route_on_validation)

    # End after research
    workflow.add_edge("classify_topic_node", "plan_node")
    workflow.add_edge("plan_node", END)

    # Compile
    app = workflow.compile()

    return app
