"""
Interview Preparation Assistant - Main Application Entry Point

This Streamlit application helps users prepare for job interviews by:
- Analyzing job descriptions from URLs
- Processing resume information from PDF files
- Using various prompt engineering strategies to generate interview preparation content
- Providing an interactive chat interface with AI assistance
"""

import streamlit as st
from utiles.show_notifications import display_notification, show_notificaton_message
from config.init import initial_session
from components.sidebar import initial_sidebar
from components.content import (
    input_system_instruction,
    input_url_content,
    resume_input_content,
    input_selected_prompt,
    review_url_extracted_content,
)
from utiles.init_llm_model import initial_llm_model
from openai.types.chat import ChatCompletionMessageParam


# Initialize session state variables before any UI rendering
initial_session()

# Configure Streamlit page settings
st.set_page_config(
    page_title="Interview",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.config_toggle else "collapsed",
)

# Apply custom CSS styling to the application
st.markdown(
    """
<style>
    html {
        font-size: 18px;
    }
</style>
""",
    unsafe_allow_html=True,
)
st.header("You are preparing now an interview!")


# Check and display any pending notifications at the top of the page
display_notification()

# Render the sidebar with API configuration and model settings
initial_sidebar()

# Render input components for job position URL
input_url_content()
review_url_extracted_content()

# Render resume PDF upload component
resume_input_content()

# Render system instruction and prompt strategy display areas
input_system_instruction()
input_selected_prompt()

# Display chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Main chat interface - handles user input and AI response generation
if prompt := st.chat_input("Input or Enter your start... "):
    # Add user message to chat history

    if st.session_state.api_key is None or st.session_state.selected_model is None:
        st.error("Please inupt API and set model at first.")
    else:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare messages for API call: system instruction + selected prompt + conversation history
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": f"{st.session_state.system_instruction}{st.session_state.selected_prompt_content}",
            }
        ]
        for m in st.session_state.messages:
            messages.append({"role": m["role"], "content": m["content"]})

        # Generate AI response
        with st.chat_message("assistant"):
            if st.session_state.selected_prompt_strategy is not None:
                if client := initial_llm_model():
                    # Create streaming chat completion with configured parameters
                    stream = client.chat.completions.create(
                        model=st.session_state.selected_model,
                        temperature=st.session_state.model_temperatur,
                        top_p=st.session_state.model_top_p,
                        #                top_k=st.session_state.model_top_k,
                        frequency_penalty=st.session_state.model_frequency_penalty,
                        presence_penalty=st.session_state.model_presence_penalty,
                        messages=messages,
                        stream=True,
                    )
                    # Display streaming response
                    response = st.write_stream(stream)
                    # Save assistant response to chat history
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    # Update message history for the selected prompt strategy
                    for (
                        strategy,
                        messages,
                    ) in st.session_state.prompt_strategies_messages[
                        ["strategy", "messages"]
                    ].values:
                        if st.session_state.selected_prompt_strategy == strategy:
                            messages = st.session_state.messages
                else:
                    show_notificaton_message(
                        "Model can't be initialized, please check the API key", 2
                    )
            else:
                show_notificaton_message(
                    "You should select a prompt strategy at first.", 2
                )
