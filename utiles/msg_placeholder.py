import streamlit as st

def get_msg_placeholder():
    """
    Get or create the message placeholder that persists across reruns.
    The placeholder must be created at the top of the app to always be visible.
    """
    if "msg_placeholder" not in st.session_state:
        st.session_state.msg_placeholder = st.empty()
    return st.session_state.msg_placeholder
