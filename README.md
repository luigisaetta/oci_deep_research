# OCI Deep Research
This repository contains the code for a concept/demo around **Deep Research**, using OCI

## Model used
The demo use:
* openai.gpt-4o-search-preview, for search
* xai.grok-3, for all the other tasks

## Implementation
The agent is implemented using **LangGraph** and OCI Generative AI (integrated with **LangChain 1.x** + `langchain-oci`).
Agent is exposed as a REST service, streaming.

UI is implemented usiong **Streamlit**.

For the dependencies see: [requirements](./requirements.txt)

The graph is defined in [agent/workflow.py](./agent/workflow.py)

## Tests
To run regression tests, install **pytest** and run

```
pytest -s tests
```
