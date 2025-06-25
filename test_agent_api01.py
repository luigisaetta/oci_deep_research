"""
Test client for the FastAPI agent.
This client sends a request to the FastAPI agent
and prints the response.

It also prints the name of the completed steps.
Some steps are repeated, as needed.

Author: L. Saetta
"""

import asyncio
import json
import httpx
from utils import get_console_logger
from config import AGENT_API_URL

logger = get_console_logger("agent_fastapi_client_logger", level="INFO")


async def stream_invoke(_user_input: str):
    """
    Stream the chat with the agent.
    Args:
        user_input (str): User input for the research agent.
    """
    # Prepare the input
    payload = {"user_input": _user_input}

    async with httpx.AsyncClient(timeout=None) as client:
        print("--------------------")
        print("Streaming response:")
        print("--------------------")

        async with client.stream("POST", AGENT_API_URL, json=payload) as response:
            async for line in response.aiter_lines():
                if line.strip():  # skip empty lines
                    try:
                        data = json.loads(line)

                        for key, value in data.items():
                            # key here is the name of the node
                            logger.info("Step: %s completed...", key)
                            logger.info("")

                            if key == "plan_node":
                                print("")
                                print("This is the plan:")
                                print("title: ", value["plan"]["title"])
                                print("")
                                for section in value["plan"]["sections"]:
                                    print(section["title"])
                                    print(section["description"])
                                    print("")

                                print("")

                            if key == "review_node":
                                # the last node
                                print("")
                                print(value["reviewed_report"])

                    except json.JSONDecodeError as e:
                        print("Failed to parse JSON:", e)


if __name__ == "__main__":

    USER_INPUT = """Generate a report regarding performances of the different LLM
    on Oracle OCI Generative AI.
    Consider only high end LLM and produce a short report, not detailed.
    """

    print("--------------------")
    print("User input:")
    print(USER_INPUT)
    print("--------------------")

    asyncio.run(stream_invoke(USER_INPUT))
