"""
The State of the graph

Author: L. Saetta
"""

from typing import TypedDict, List, Dict


class ReportState(TypedDict):
    """
    The State of the graph
    """

    # subject proposed by the user
    subject: str

    # to handle clarification requests (added 26/06/2025)
    clarification_needed: bool
    clarification_request: str
    system_messages: list  # list of HumanMessage or AIMessage

    # topic identified (classify_node)
    topic: str
    # lengt of the report (medium, long)
    report_length: str

    plan: Dict
    sections: List[Dict]

    current_section: int
    section_drafts: List[str]

    retrieved_info: str

    # the assembled report
    full_report: str

    # the final report, after LLM review
    reviewed_report: str
