# tests/test_validate_request_node.py

import pytest
from agent.validate_request import ValidateRequest

@pytest.fixture
def node():
    return ValidateRequest()


class _FakeResponse:
    def __init__(self, content):
        self.content = content


class _FakeLLM:
    def __init__(self, responses):
        self._responses = responses
        self._idx = 0

    def invoke(self, _prompt):
        response = self._responses[self._idx]
        self._idx += 1
        return _FakeResponse(response)


def test_clear_request(node, monkeypatch):
    # clear request -> decision yes, then summary returned
    fake_llm = _FakeLLM(
        [
            '{"decision":"yes"}',
            "Create a detailed report on the LangGraph agentic framework.",
        ]
    )
    monkeypatch.setattr("agent.validate_request.get_chat_model", lambda: fake_llm)

    input_data = {
        "subject": "Create a detailed and complete report on the LangGraph agentic framework.",
        "chat_history": [],
    }
    output = node.invoke(input_data)

    assert output["clarification_needed"] is False
    assert output["subject"] == "Create a detailed report on the LangGraph agentic framework."


def test_not_so_clear_request(node, monkeypatch):
    # unclear request -> decision no and clarification question
    fake_llm = _FakeLLM(
        [
            '{"decision":"no","clarification_request":"Do you want architecture, use cases, or implementation details?"}'
        ]
    )
    monkeypatch.setattr("agent.validate_request.get_chat_model", lambda: fake_llm)

    input_data = {
        "subject": "Explain LangGraph workflows, create a detailed report.",
        "chat_history": [],
    }
    output = node.invoke(input_data)

    assert output["clarification_needed"] is True
    assert output["clarification_request"] is not None


def test_unclear_request(node, monkeypatch):
    fake_llm = _FakeLLM(
        [
            '{"decision":"no","clarification_request":"Which LangGraph area are you interested in?"}'
        ]
    )
    monkeypatch.setattr("agent.validate_request.get_chat_model", lambda: fake_llm)

    input_data = {
        "subject": "I want some information regarding LangGraph, but not sure which area",
        "chat_history": [],
    }
    output = node.invoke(input_data)

    assert output["clarification_needed"] is True
    assert output["clarification_request"] is not None
