import streamlit as st


def set_tempertur():
    temperatur = st.slider(
        "Select the temperatur of model",
        min_value=0.0,
        max_value=1.0,
        step=0.01,
        value = 0.0,
        help="Control the randomness of generated answer!"
    )
    st.session_state.model_temperatur = temperatur


def set_top_p():
    top_p = st.slider(
        "Select the top p of model",
        min_value=1,
        max_value=50,
        step=1,
        value = 1,
        help="Set the nucleus sampling of considerable answers."
    )
    st.session_state.model_top_p = top_p
    

def set_top_k():
    top_k = st.slider(
        "Select the top k of model",
        min_value=1,
        max_value=10,
        step=1,
        value = 1,
        help="set the number of allowed answers!"
    )
    st.session_state.model_top_k = top_k
    


def set_fequency_penalty():
    fequency_penalty = st.slider(
        "Select the fequency penalty of model",
        min_value=-2.0,
        max_value=2.0,
        step=0.1,
        value = 0.0,
        help="Set the penalty of repetition to token!"
    )
    st.session_state.fequency_penalty = fequency_penalty

def set_presence_penalty():
    presence_penalty = st.slider(
        "Select the presence penalty of model",
        min_value=-2.0,
        max_value=2.0,
        step=0.1,
        value = 0.0,
        help="Set the penalty of repetition to answers!"
    )
    st.session_state.presence_penalty = presence_penalty    
