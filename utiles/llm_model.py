from openai import OpenAI
import streamlit as st


def initial_llm_model():
    if st.session_state.api_key is not None:
        client = OpenAI(api_key = st.session_state.api_key)
        return client
    else:
        return None

def url_input_analysis(url_content):
    client = initial_llm_model()

    if client is None:
        return None
    
    response = client.chat.completions.create(
        model = st.session_state.selected_model,
        messages = [
            {"role": "system", "content": "You are a very helpful assistant, please extract the complete position informatoin, without any imgaes included, and then convert it into markdown format, please be careful and think hard, you have to return valid markdown format."},
            {"role": "user", "content": url_content}
        ],
        stream = True
    )
    return response

