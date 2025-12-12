"""
Session state initialization for the interview preparation application.

This module initializes all session state variables with default values
at application startup. Session state persists data across Streamlit reruns.
"""

import streamlit as st
import pandas as pd
from .variables import init_prompt_content


def initial_session():
    """
    Initialize all session state variables with default values.

    This function sets up:
    - API configuration (key, available models, selected model)
    - Model hyperparameters (temperature, top_p, top_k, penalties)
    - UI state (toggles, notifications)
    - Chat state (messages, conversation history)
    - Prompt strategies (predefined prompt templates and their message histories)
    - Content storage (position description, resume text)

    Only initializes variables that don't already exist in session state,
    preserving existing values across reruns.
    """
    if "api_key" not in st.session_state:
        st.session_state.api_key = None

    if "config_toggle" not in st.session_state:
        st.session_state.config_toggle = True

    if "update_api_key" not in st.session_state:
        st.session_state.update_api_key = False

    if "available_model" not in st.session_state:
        st.session_state.available_model = None

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = None

    if "model_temperatur" not in st.session_state:
        st.session_state.model_temperatur = 1.0

    if "model_top_p" not in st.session_state:
        st.session_state.model_top_p = 1.0

    if "model_top_k" not in st.session_state:
        st.session_state.model_top_k = 1

    if "model_frequency_penalty" not in st.session_state:
        st.session_state.model_frequency_penalty = 0.0

    if "model_presence_penalty" not in st.session_state:
        st.session_state.model_presence_penalty = 0.0

    if "notification_message_content" not in st.session_state:
        st.session_state.notification_message_content = ""

    if "notification_message_time" not in st.session_state:
        st.session_state.notification_message_time = 0

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "selected_prompt_content" not in st.session_state:
        st.session_state.selected_prompt_content = None

    if "selected_prompt_strategy" not in st.session_state:
        st.session_state.selected_prompt_strategy = None

    if "review_url_content" not in st.session_state:
        st.session_state.review_url_content = False

    if "review_pdf_content" not in st.session_state:
        st.session_state.review_pdf_content = False

    if "action_llm_phase_url" not in st.session_state:
        st.session_state.action_llm_phase_url = False

    if "toggle_input_pdf" not in st.session_state:
        st.session_state.toggle_input_pdf = False

    if "position_description" not in st.session_state:
        st.session_state.position_description = ""

    if "resume_description" not in st.session_state:
        st.session_state.resume_description = ""

    (
        standard_prompt_content,
        zero_shot_prompt_content,
        one_shot_prompt_content,
        few_shot_prompt_content,
        CoT_prompt_content,
        delimiter_prompt_content,
    ) = init_prompt_content()
    if "prompt_strategies" not in st.session_state:
        data = [
            {
                "strategy": "standard prompt ",
                "content": standard_prompt_content,
            },
            {
                "strategy": "zero shot prompt ",
                "content": zero_shot_prompt_content,
            },
            {
                "strategy": "one shot prompt",
                "content": one_shot_prompt_content,
            },
            {
                "strategy": "few shot prompt",
                "content": few_shot_prompt_content,
            },
            {
                "strategy": "Chain of Thought",
                "content": CoT_prompt_content,
            },
            {
                "strategy": "delimiter prompt",
                "content": delimiter_prompt_content,
            },
        ]
        st.session_state.prompt_strategies = pd.DataFrame(data)

    if "prompt_strategies_messages" not in st.session_state:
        data = [
            {
                "strategy": "standard prompt ",
                "messages": [],
            },
            {
                "strategy": "zero shot prompt ",
                "messages": [],
            },
            {
                "strategy": "one shot prompt",
                "messages": [],
            },
            {
                "strategy": "few shot prompt",
                "messages": [],
            },
            {
                "strategy": "Chain of Thought",
                "messages": [],
            },
            {
                "strategy": "delimiter prompt",
                "messages": [],
            },
        ]
        st.session_state.prompt_strategies_messages = pd.DataFrame(data)


def init_msg_placeholder():
    """
    Get or create the message placeholder that persists across reruns.
    The placeholder must be created at the top of the app to always be visible.
    """
    if "msg_placeholder" not in st.session_state:
        st.session_state.msg_placeholder = st.empty()
    return st.session_state.msg_placeholder
