import streamlit as st
import pandas as pd


def initial_session():
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    
    if "config_toggle" not in st.session_state:
        st.session_state.config_toggle = True

    if "update_api_key" not in st.session_state:
        st.session_state.update_api_key = False

    if "available_model" not in st.session_state:
        st.session_state.available_model = None
        
    if "select_model" not in st.session_state:
        st.session_state.select_model = None

    if "model_temperatur" not in st.session_state:
        st.session_state.model_temperatur = None

    if "model_top_p" not in st.session_state:
        st.session_state.model_top_p = None        

    if "model_fequency_penalty" not in st.session_state:
        st.session_state.model_fequency_penalty = None        

    if "model_presence_penalty" not in st.session_state:
        st.session_state.model_presence_penalty = None        

    if "notification_message_content" not in st.session_state:
        st.session_state.notification_message_content = None

    if "notification_message_time" not in st.session_state:
        st.session_state.notification_message_time = 0

    if "position_description" not in st.session_state:
        st.session_state.position_description = None
        
    if "resume_description" not in st.session_state:
        st.session_state.resume_description = None

    if "messages" not in st.session_state:
        st.session_state.messages = []


    if "prompt_strategies" not in st.session_state:
        data = [
            {
                "strategy": "zero-shot",
                "content": "please help me to solve the problem",
            },
            {
                "strategy": "one-shot",
                "content": "please help me to solve the problem, such as how can I prepare it for my technical skills",
            },
        ]
        st.session_state.prompt_strategies = pd.DataFrame(data)

    if "selected_prompt_content" not in st.session_state:
        st.session_state.selected_prompt_content = None

    if "selected_prompt_strategy" not in st.session_state:
        st.session_state.selected_prompt_strategy = None
        

