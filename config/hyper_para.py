"""
Hyperparameter configuration components for LLM models.

This module provides UI components (sliders) for adjusting various
hyperparameters that control the behavior of language model generation.
"""

import streamlit as st


def set_tempertur():
    """
    Create a slider for adjusting model temperature.
    
    Temperature controls the randomness of the model's output:
    - Lower values (closer to 0): More focused and deterministic
    - Higher values (closer to 2): More random and creative
    
    Updates: st.session_state.model_temperatur
    """
    temperatur = st.slider(
        "Select the temperatur of model",
        min_value=0.0,
        max_value=2.0,
        step=0.1,
        value=1.0,
        help="Control the randomness of generated answer!",
    )
    st.session_state.model_temperatur = temperatur


def set_top_p():
    """
    Create a slider for adjusting nucleus sampling (top-p).
    
    Top-p sampling considers only the smallest set of tokens whose
    cumulative probability exceeds p. This limits the token pool
    to the most likely candidates.
    
    Updates: st.session_state.model_top_p
    """
    top_p = st.slider(
        "Select the top p of model",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        value=1.0,
        help="Set the nucleus sampling of considerable answers.",
    )
    st.session_state.model_top_p = top_p


def set_top_k():
    """
    Create a slider for adjusting top-k sampling.
    
    Top-k limits the number of highest probability tokens to consider
    for each generation step. Lower values make output more focused.
    
    Updates: st.session_state.model_top_k
    """
    top_k = st.slider(
        "Select the top k of model",
        min_value=1,
        max_value=10,
        step=1,
        value=1,
        help="set the number of allowed answers!",
    )
    st.session_state.model_top_k = top_k


def set_frequency_penalty():
    """
    Create a slider for adjusting frequency penalty.
    
    Frequency penalty reduces the likelihood of repeating the same tokens.
    Positive values discourage repetition, negative values encourage it.
    
    Updates: st.session_state.frequency_penalty
    """
    frequency_penalty = st.slider(
        "Select the frequency penalty of model",
        min_value=-2.0,
        max_value=2.0,
        step=0.1,
        value=0.0,
        help="Set the penalty of repetition to token!",
    )
    st.session_state.frequency_penalty = frequency_penalty


def set_presence_penalty():
    """
    Create a slider for adjusting presence penalty.
    
    Presence penalty reduces the likelihood of repeating topics/themes.
    Positive values encourage exploring new topics, negative values
    allow more focus on existing topics.
    
    Updates: st.session_state.presence_penalty
    """
    presence_penalty = st.slider(
        "Select the presence penalty of model",
        min_value=-2.0,
        max_value=2.0,
        step=0.1,
        value=0.0,
        help="Set the penalty of repetition to answers!",
    )
    st.session_state.presence_penalty = presence_penalty
