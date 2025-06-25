"""
The State of the graph
"""

from typing import TypedDict, List, Dict


class ReportState(TypedDict):
    """
    The State of the graph
    """

    # subject proposed by the user
    subject: str
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
