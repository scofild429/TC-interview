"""
Dialog components for configuration management.

This module provides dialog windows for:
- API key deletion confirmation
- Model hyperparameter adjustment
"""

import streamlit as st
from config.hyper_para import (
    set_frequency_penalty,
    set_presence_penalty,
    set_tempertur,
    set_top_k,
    set_top_p,
)
from utiles.show_notifications import show_notificaton_message


@st.dialog("Delete API Key")
def open_delete_api_dialog():
    """
    Display a confirmation dialog for deleting the stored API key.

    Presents a warning message with Yes/Cancel options. If confirmed:
    - Resets API key and model configuration
    - Shows the API configuration sidebar
    - Displays a success notification
    """
    st.write("Are you sure you delete your API key? This cannot be undone.")

    col1, _, col2 = st.columns([1, 3, 1])

    with col1:
        if st.button("Yes", type="primary"):
            st.session_state.config_toggle = True
            st.session_state.update_api_key = False
            st.session_state.api_key = None
            st.session_state.available_model = None
            st.session_state.selected_model = None
            show_notificaton_message("Your API key has been successful removed", 2)
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.rerun()


@st.dialog("Adjust the model")
def open_model_config_dialog():
    """
    Display a dialog for adjusting model inference parameters.

    Provides sliders for configuring:
    - Temperature: Controls randomness of responses
    - Top-k: Number of token candidates to consider
    - Top-p: Nucleus sampling threshold
    - Frequency penalty: Reduces repetition of tokens
    - Presence penalty: Reduces repetition of topics
    """
    set_tempertur()
    set_top_k()
    set_top_p()
    set_frequency_penalty()
    set_presence_penalty()
