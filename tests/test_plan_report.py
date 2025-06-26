# tests/test_validate_request_node.py

import pytest
from report_state import ReportState
from plan_report_node import PlanReportNode

@pytest.fixture
def node():
    return PlanReportNode()

def test_ok_request(node):
    state = ReportState(subject="LangGraph agentic framework", 
                        report_length="medium", 
                        topic="AI frameworks")
    
    output = node.invoke(state)
    
    assert output["plan"] is not None
    assert output["sections"] is not None

