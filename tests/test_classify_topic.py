# tests/test_validate_request_node.py

import pytest
from oci_deep_research.report_state import ReportState
from oci_deep_research.classify_topic_node import ClassifyTopicNode

@pytest.fixture
def node():
    return ClassifyTopicNode()

def test_ok_request(node):
    state = ReportState(subject="LangGraph agentic framework")
    
    output = node.invoke(state)
    
    assert output["topic"] is not None
    assert output["report_length"] is not None

