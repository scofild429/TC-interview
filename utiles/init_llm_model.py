"""
LLM client initialization and management.

This module handles:
- OpenAI client creation and initialization
- URL content analysis using LLM (deprecated function)
"""

from openai import OpenAI
import streamlit as st


def initial_llm_model():
    """
    Initialize and return OpenAI client if API key is available.

    Returns:
        OpenAI: Configured OpenAI client instance
        None: If no API key is set in session state

    This function is called throughout the application whenever
    API access is needed for chat completions or other operations.
    """
    if st.session_state.api_key is not None:
        client = OpenAI(api_key=st.session_state.api_key)
        return client
    else:
        return None
