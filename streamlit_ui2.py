"""
Streamlit UI for Workflow2
"""

import uuid
from typing import List, Union
import time
import streamlit as st

from langchain_core.messages import HumanMessage, AIMessage
from report_state import ReportState
from workflow2 import create_workflow

from utils import get_console_logger

# Constant

# name for the roles
USER = "user"
ASSISTANT = "assistant"

logger = get_console_logger(name="UI")


# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "workflow" not in st.session_state:
    # the agent instance
    st.session_state.workflow = create_workflow()
if "thread_id" not in st.session_state:
    # generate a new thread_Id
    st.session_state.thread_id = str(uuid.uuid4())


#
# supporting functions
#
def display_msg_on_rerun(chat_hist: List[Union[HumanMessage, AIMessage]]) -> None:
    """Display all messages on rerun."""
    for msg in chat_hist:
        role = USER if isinstance(msg, HumanMessage) else ASSISTANT
        with st.chat_message(role):
            st.markdown(msg.content)


# when push the button reset the chat_history
def reset_conversation():
    """Reset the chat history."""
    st.session_state.chat_history = []

    # change thread_id
    st.session_state.thread_id = str(uuid.uuid4())


def add_to_chat_history(msg):
    """
    add the msg to chat history
    """
    st.session_state.chat_history.append(msg)


def get_chat_history():
    """return the chat history from the session"""
    return st.session_state.chat_history


#
# Main
#
st.title("📘 OCI Deep Research")

# Reset button
if st.sidebar.button("Clear Chat History"):
    reset_conversation()


#
# Here the code where react to user input
#

# Display chat messages from history on app rerun
display_msg_on_rerun(get_chat_history())

if question := st.chat_input("Hello, how can I help you?"):
    # Display user message in chat message container
    st.chat_message(USER).markdown(question)

    try:
        with st.spinner("Calling AI..."):
            time_start = time.time()

            # get the chat history to give as input to LLM
            _chat_history = get_chat_history()

            # modified to be more responsive, show result asap
            try:
                input_state = ReportState(
                    subject=question,
                )

                # set the agent config
                agent_config = {
                    "configurable": {
                        "thread_id": st.session_state.thread_id,
                    }
                }

                # loop to manage streaming
                last_state = None
                for event in st.session_state.workflow.stream(
                    input_state,
                    config=agent_config,
                ):
                    # display feedback on step completed
                    for key, value in event.items():
                        MSG = f"Completed: {key}!"
                        logger.info(MSG)
                        st.toast(MSG)

                        last_state = value

                if last_state.get("clarification_needed", True):
                    # if clarification is needed, show the request
                    ANSWER = last_state.get("clarification_request", "")
                else:
                    # fow now
                    ANSWER = "Topic is: " + last_state["topic"]

                with st.chat_message(ASSISTANT):
                    response_container = st.empty()
                    response_container.markdown(ANSWER)

                # Add user/assistant message to chat history
                add_to_chat_history(HumanMessage(content=question))
                add_to_chat_history(AIMessage(content=ANSWER))

            except Exception as e:
                ERR_MSG = f"Error in Deep Research UI: {e}"
                logger.error(ERR_MSG)
                st.error(ERR_MSG)

    except Exception as e:
        ERR_MSG = "Error in Deep Research UI: " + str(e)
        logger.error(ERR_MSG)
        st.error(ERR_MSG)
