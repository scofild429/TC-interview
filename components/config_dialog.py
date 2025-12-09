import streamlit as st
from .hyper_para import set_fequency_penalty, set_presence_penalty, set_tempertur, set_top_k, set_top_p
from utiles.notifications import show_notificaton_message

@st.dialog("Delete API Key")
def open_delete_api_dialog():
    st.write("Are you sure you delete your API key? This cannot be undone.")
    
    col1, _, col2 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("Yes", type="primary"):
            st.session_state.config_toggle = True
            st.session_state.update_api_key = False
            st.session_state.api_key = None
            st.session_state.available_model = None
            st.session_state.select_model = None
            show_notificaton_message("Your API key has been successful removed", 2)
            st.rerun()
    with col2:
        if st.button("Cancel"):
            st.rerun()

@st.dialog("Adjust the model")
def open_model_config_dialog():
    set_tempertur()
    set_top_k()
    set_top_p()
    set_fequency_penalty()
    set_presence_penalty()
    

