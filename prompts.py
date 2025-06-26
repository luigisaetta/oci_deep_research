"""
Prompts

In this file are defined the prompts used in the application.

Author: L. Saetta
"""

# prompt to classify the request and identify the topic and report length
PROMPT_TEMPLATE_TOPIC = """
Classify the topic for a research report on: {subject}.
Use only one or a few words as topic name.
Classify also the report length requested: can be only one of: short, medium, long.
Default length is: medium. 
If the requst asks for a detailed report, classify it as long.
If the request asks for a brief report, classify it as short.

Respond as JSON.
Enclose the JSON in triple backtics.

Example:
```json
{{
    "topic": "Generative AI",
    "report_length": "long"
}}
```
"""

# prompt used to define the invocation to LLM used also for search
PROMPT_TEMPLATE_SEARCH = """
Provide key points and summaries from credible sources about: {section}.
Topic: {subject}
"""

# for the generate section node
PROMPT_TEMPLATE_GENERATE = """
Write the section titled "{section}" for a research report.
Base it on this information:
{retrieved_info}
Write in a clear and formal style.
Report also all the sources used in the section.
"""

# for the repoirt review node
PROMPT_TEMPLATE_REVIEW = """
You are an expert writing assistant. 
Your task is to revise and improve the following research report.

* Do not remove or alter any core concepts.
* Eliminate redundancies and repetitive phrasing.
* Improve clarity, flow, and sentence structure.
* Use a formal, professional tone suitable for publication.

Below is the full report to review:
---
{full_report}
"""

PROMPT_TEMPLATE_PLAN = """
Create a detailed outline for a research report on: {subject}.
Include:
- Title
- {min_sections} to {max_sections} sections with brief descriptions
- for each section: title and description
Respond as JSON.
Enclose the JSON in triple backtics.

Example:
```json
{{
"title": "Evaluating High-End Large Language Models on Oracle OCI Generative AI: A Performance Comparison",
"sections": [
    {{
    "title": "Introduction",
    "description": "This section introduces the context and purpose of the report, highlighting..."
    }},
    {{
    "title": "Methodology",
    "description": "This section outlines the methodology used to ..."
    }},
    {{
    "title": "LLM Models and Configurations",
    "description": "This section provides an in-depth description of the ..."
    }}
]
}}
```
"""

PROMPT_TEMPLATE_VALIDATE_REQUEST = """
You are an assistant that determines if a user request is clear enough to start structured research.
If the request is specific and clear enough to proceed without further clarification, respond with 'yes'.
If the request is not clear, respond with 'no'. In this case provide also a request for clarification.
Do not add any comment or other detail.
Respond as JSON.
Enclose the JSON in triple backtics.

Example:
```json
{{
    "decision": "no",
    "clarification_request": "Please provide more details about the specific aspects of the LangGraph."
}}
```

User request:
{user_input}
"""
