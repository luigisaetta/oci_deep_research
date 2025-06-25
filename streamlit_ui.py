"""
Streamlit UI

Author: L. Saetta
"""

import asyncio
import json
import httpx
import streamlit as st
from config import AGENT_API_URL, DEFAULT_MAX_SECTIONS


# helper functions
def generate_pretty_sections(sections):
    """
    Generate a better representation of the sections
    """
    pretty_sections = []

    for section in sections:
        title = section.get("title", "Untitled Section")
        description = section.get("description", "No description provided.")
        pretty_sections.append({"title": title, "description": description})

    return pretty_sections


# Streamlit UI
st.set_page_config(page_title="Research Agent", layout="centered")
st.title("📘 OCI Deep Research")
st.markdown(
    "Enter a subject to generate a report using an **AI agent** and **Internet Search**."
)

# SIDEBAR
st.sidebar.title("Information")
st.sidebar.header("Progress:")
progress = st.sidebar.progress(0)

# Central area
user_input = st.text_area("🔍 Research Topic", height=150)
start_button = st.button("Generate Report")

if start_button and user_input.strip():
    with st.spinner("Generating... this might take some minutes ⏳"):
        report_placeholder = st.empty()
        report_lines = []

        async def stream_invoke(_user_input: str):
            """
            Invoke in streaming mode
            """
            payload = {"user_input": _user_input}

            async with httpx.AsyncClient(timeout=None) as client:
                async with client.stream(
                    "POST", AGENT_API_URL, json=payload
                ) as response:
                    # process the streaming response
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                data = json.loads(line)

                                # only as safe value
                                n_sections = DEFAULT_MAX_SECTIONS

                                for key, value in data.items():
                                    # report the completed node
                                    step_name = key

                                    #
                                    # Node: plan_node
                                    #
                                    if key == "plan_node":
                                        # show on the screen the plan with sections
                                        _pretty_sections = generate_pretty_sections(
                                            value["sections"]
                                        )
                                        # after planning compute the actual value
                                        n_sections = len(_pretty_sections)

                                        st.sidebar.header("Report sections:")
                                        st.sidebar.json(
                                            str(_pretty_sections),
                                            expanded=False,
                                        )

                                    #
                                    # Node: search_node, generate_node
                                    #
                                    if key in ["search_node", "generate_node"]:
                                        try:
                                            # add the title of the document section
                                            step_name += (
                                                ", "
                                                + value["sections"][
                                                    value["current_section"]
                                                ]["title"]
                                            )
                                            # update progress
                                            progress_fraction = (
                                                value["current_section"] / n_sections
                                            )
                                            progress.progress(progress_fraction)
                                        except Exception:
                                            # quick fix
                                            pass

                                    #
                                    # Node: review_node
                                    #
                                    if key == "review_node":
                                        # the last node
                                        report_lines.append(value["reviewed_report"])
                                        report_placeholder.markdown(
                                            f"### 📄 Final Report\n\n{value['reviewed_report']}"
                                        )
                                        # finished, update the progress bar
                                        progress.progress(100)

                                    st.toast(f"Completed: {step_name}")

                            except json.JSONDecodeError:
                                continue

        asyncio.run(stream_invoke(user_input))
