"""
Test Agent

Author: L. Saetta
"""

from report_state import ReportState
from workflow import create_workflow

agent = create_workflow()

INPUT = "Create a report comparing Anthropic and Langchain approach to AI Agents."

initial_state = ReportState(subject=INPUT)
response = agent.invoke(initial_state)

print("")
print("Agent output:")
print(response["full_report"])
print("")
