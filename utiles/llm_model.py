from openai import OpenAI
import streamlit as st


def url_input_analysis(url_content):
    response = None
    if st.session_state.api_key:
        client = OpenAI(api_key = st.session_state.api_key)
        response = client.chat.completions.create(
            model = st.session_state.select_model,
            messages = [
                {"role": "system", "content": "You are a very helpful assistant, please extract the complete position informatoin, without any imgaes included, and then convert it into markdown format, please be careful and think hard, you have to return valid markdown format."},
                {"role": "user", "content": url_content}
            ],
            stream = True
        )
    return response
    
    
