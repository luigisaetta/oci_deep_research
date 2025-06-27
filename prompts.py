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
You are an assistant that evaluates whether a user’s request is sufficiently defined to begin structured research.

Instructions:
1. If the user’s request is specific and clear enough to proceed, respond with:
   {{
     "decision": "yes",
     "clarification_request": null
   }}

2. If the request is ambiguous or lacks essential details, respond with:
   {{
     "decision": "no",
     "clarification_request": "<your question asking for the missing detail(s)>"
   }}

   The clarification should:
   - Explain that as an assistant you can help research and prepare a report based on the findings.
   - Identify exactly what additional information is needed to proceed.

3. If the request is about what you can do, respond with:
   {{
     "decision": "no",
     "clarification_request": 
     "Explain that you are an assistant that can help in doing research and creating reports based on the results."
   }}

Format Requirements:
- Always output valid JSON.
- Enclose the JSON response in triple backticks (```).

Example:

User: "Tell me about LangGraph."
Assistant:
```json
{{
  "decision": "no",
  "clarification_request": "Could you clarify which aspects of LangGraph you're interested in—architecture, comparison with other tools, or real‑world use cases? I can help research and compile a report once I know."
}}
```

Chat history:
{chat_history}

User request:
{user_input}
"""

# prompt to summarize the user request and chat history
PROMPT_TEMPLATE_SUMMARIZE_REQUEST = """
You are an assistant that summarizes a conversation into a short subject for a research report.

Chat history:
{chat_history}

User request:
{user_request}

Provide the summary in one concise sentence.
"""
