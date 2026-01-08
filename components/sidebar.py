"""
Sidebar component for application configuration.

This module provides the sidebar UI containing:
- API key input and validation
- Model selection dropdown
- API key management (change/delete)
- Model inference settings
- Prompt strategy selection
"""

import streamlit as st
from utiles.check_api import check_api_key, check_api_key_function
from components.dialogs import open_model_config_dialog, open_delete_api_dialog
from utiles.actions import change_prompt_strategy, Generate_Application_PDF


def initial_sidebar():
    """
    Render the application sidebar with configuration options.

    The sidebar has two states:
    1. Configuration mode (config_toggle=True): Shows API key input
    2. Normal mode (config_toggle=False): Shows model settings and controls

    In normal mode, provides:
    - Model selection dropdown
    - API key change/delete buttons
    - Inference settings configuration
    - Prompt strategy selector
    """
    with st.sidebar:
        if st.session_state.config_toggle:
            st.header("API KEY Configuration")

            st.text_input(
                "OpenAI API key",
                type="password",
                key="input_api_key",
                on_change=check_api_key,
                help="please provide your api key",
            )
        else:
            st.header("Model Configuration")
            avaliable_model = st.session_state.available_model
            selected_model = st.selectbox(
                "Choose an available AI model",
                avaliable_model,
            )
            st.session_state.selected_model = selected_model

            st.divider()
            if st.button("Change API Key"):
                st.session_state.update_api_key = not st.session_state.update_api_key
                #                st.rerun()
            if st.session_state.update_api_key:
                value = st.text_input("Enter your new API Key", type="password")
                if value:
                    st.session_state.update_api_key = False
                    check_api_key_function(value)
                    #                    st.rerun()

            if st.button("Delete API Key", type="primary"):
                open_delete_api_dialog()

            st.divider()
            if st.button("Inference settings"):
                open_model_config_dialog()

            st.selectbox(
                "Choose prompt strategy",
                st.session_state.prompt_strategies.strategy,
                key="selected_prompt_strategy",
                on_change=change_prompt_strategy,
            )

            if st.button("Generate Application", type="primary"):
                if st.session_state.resume_description != "" and st.session_state.position_description != "":
                    Generate_Application_PDF()
