"""
Agent API

Author: L. Saetta
"""

import uuid
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from .workflow import create_workflow
from .report_state import ReportState
from .utils import get_console_logger
from .config import DEBUG

MEDIA_TYPE = "application/json"


class InvokeRequest(BaseModel):
    """
    This class represent the input
    """

    user_input: str


app = FastAPI()

# here we create the graph
agent_graph = create_workflow()

logger = get_console_logger("agent_fastapi_logger", level="INFO")


def generate_request_id():
    """
    Generate a unique request id

    Returns:
        str: A unique identifier for the request.
    """
    return str(uuid.uuid4())


async def stream_graph_updates(user_input: str, config=None):
    """
    Stream the updates from the deep research agent graph.
    Args:
        user_input (str): User input for the agent.
    Yields:
        str: JSON string of the step output.
    """
    # prepare the input
    state = ReportState(subject=user_input)

    # here we call the agent and return the state
    # update the state with the user input
    async for step_output in agent_graph.astream(state, config=config):
        # using stream with LangGraph returns state updates
        # for each node in the graph
        yield json.dumps(step_output) + "\n"


@app.post("/invoke")
async def invoke(request: InvokeRequest):
    """
    POST endpoint to interact with the Deep Research agent.
    Args:
        request (InvokeRequest): Contains the user_input as JSON body.
    Returns:
        StreamingResponse: Stream of JSON responses from the agent.
    """
    _thread_id = generate_request_id()
    _config = {"configurable": {"thread_id": _thread_id}}

    if DEBUG:
        logger.info("Invoked Agent API with config: %s", _config)

    try:
        # added to make it more reliable
        response = stream_graph_updates(request.user_input, _config)
    except Exception as e:
        logger.error("Error in invoke endpoint: %s", e)
        response = json.dumps({"error": str(e)})

    return StreamingResponse(response, media_type=MEDIA_TYPE)
