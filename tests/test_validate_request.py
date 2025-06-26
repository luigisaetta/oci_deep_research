# tests/test_validate_request_node.py

import pytest
from validate_request import ValidateRequest

@pytest.fixture
def node():
    return ValidateRequest()

def test_clear_request(node):
    input_data = {"subject": "Create a detailed and complete report on the LangGraph agentic framework."}
    output = node.invoke(input_data)
    
    assert output["clarification_needed"] is False

def test_not_so_clear_request(node):
    input_data = {"subject": "Explain LangGraph workflows, create a detailed report."}
    output = node.invoke(input_data)
    
    assert output["clarification_needed"] is True
    assert output["clarification_request"] is not None

def test_unclear_request(node):
    input_data = {"subject": "I want some information regarding LangGraph, but not sure which area"}
    output = node.invoke(input_data)
    
    assert output["clarification_needed"] is True
    assert output["clarification_request"] is not None

