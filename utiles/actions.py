"""
Action handlers for user interactions in the interview preparation application.

This module contains callback functions that handle various user actions such as:
- Changing prompt strategies
- Toggling content review panels
- Processing URLs to extract job descriptions
- Handling PDF resume uploads
"""
from utiles.prompts import typst_content, tone_setting

import streamlit as st
from io import StringIO
from .llm_model import initial_llm_model
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from config.variables import assemble_prompt_content



def change_prompt_strategy():
    """
    Handle prompt strategy selection change.

    Updates the selected prompt content based on the chosen strategy and
    restores the conversation history associated with that strategy.
    This allows users to switch between different prompt engineering approaches
    while maintaining separate conversation contexts.
    """
    assemble_prompt_content()
    if st.session_state.selected_prompt_strategy is not None:
        for strategy, content in st.session_state.prompt_strategies[
            ["strategy", "content"]
        ].values:
            if st.session_state.selected_prompt_strategy == strategy:
                st.session_state.selected_prompt_content = content

        for strategy, messages in st.session_state.prompt_strategies_messages[
            ["strategy", "messages"]
        ].values:
            if st.session_state.selected_prompt_strategy == strategy:
                st.session_state.messages = messages


def toggle_review_url_content():
    """
    Toggle the visibility of the URL content review panel.

    Switches the state to show/hide the extracted job description from the URL.
    """
    st.session_state.review_url_content = not st.session_state.review_url_content


def toggel_review_pdf_content():
    """
    Toggle the visibility of the PDF content review panel.

    Switches the state to show/hide the extracted resume text from the uploaded PDF.
    """
    st.session_state.review_pdf_content = not st.session_state.review_pdf_content


def toggle_llm_phase_url():
    """
    Set flag to trigger LLM processing of the input URL.

    This callback is triggered when the URL input field changes,
    signaling that the URL should be processed by the LLM.
    """
    if st.session_state.api_key is None or st.session_state.selected_model is None:
        st.error("Please input API and set model at first.")
        return

    st.session_state.action_llm_phase_url = True


def llm_phase_url():
    """
    Process a job posting URL using LLM to extract and format position information.

    This function:
    1. Validates the URL format
    2. Fetches the web page content
    3. Uses OpenAI API to extract position information
    4. Converts the extracted content to markdown format
    5. Displays the result and stores it in session state

    Handles various errors including HTTP errors, connection issues, and timeouts.
    """
    url_input = st.session_state.input_url
    if url_input:
        if not url_input.startswith("http"):
            st.error("Your URL should start with 'http' or 'https'")
        else:
            try:
                with st.spinner(f"Querying {url_input}"):
                    response = requests.get(url_input, timeout=5)
                    response.raise_for_status()

                    client = initial_llm_model()
                    if client is None:
                        return None

                    response = client.chat.completions.create(
                        model=st.session_state.selected_model,
                        messages=[
                            {
                                "role": "system",
                                "content": "You are a very helpful assistant, please extract the complete position information, without any images included, and then convert it into markdown format, please be careful and think hard, you have to return valid markdown format.",
                            },
                            {"role": "user", "content": response.text},
                        ],
                        stream=True,
                    )
                    full_text_capture = StringIO()
                    display_chunks = []

                    for chunk in response:
                        chunk_content = chunk.choices[0].delta.content or ""
                        full_text_capture.write(chunk_content)
                        display_chunks.append(chunk)

                    with st.container(height=500):
                        st.write_stream(display_chunks)

                    final_content_string = full_text_capture.getvalue()
                    st.session_state.position_description = final_content_string

            except HTTPError as http_err:
                # Handles 4xx (Client Error) and 5xx (Server Error)
                st.error(
                    f"❌ HTTP Error: The server returned code{http_err.response.status_code}"
                )
                st.code(str(http_err), language="bash")

            except ConnectionError:
                # Handles DNS failures or refused connections
                st.error("❌ Connection Error: Could not reach the server.")

            except Timeout:
                # Handles cases where the server is too slow
                st.error(
                    "❌ Timeout: The server took too long to respond (>5 seconds)."
                )

            except RequestException as e:
                # Catch-all for any other weird requests-related errors
                st.error(f"❌ An unexpected error occurred: {e}")


def llm_parse_pdf(content):
    client = initial_llm_model()
    if client is None:
        return None
    try:
        response = client.chat.completions.create(
            model=st.session_state.selected_model,
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a PDF-to-Markdown conversion assistant. "
                        "Reformat the raw text into clean, valid Markdown. "
                        "Maintain headers, lists, and tables. "
                        "Do not include any introductory text or backtick fences—return ONLY the markdown."
                    )
                },
                {"role": "user", "content": content},
            ],
         )
        
        # Correct way to access the string content
        return response.choices[0].message.content

    except Exception as e:
        st.error(f"Error calling LLM: {e}")
        return ""                
                

def parse_pdf():
    """
    Set flag to trigger PDF processing.

    This callback is triggered when a PDF file is uploaded,
    signaling that the PDF content should be extracted.
    """
    st.session_state.toggle_input_pdf = True



def Generate_Application_PDF():
    client = initial_llm_model()
    
    # 1. The Prompting Phase
    prompt = f"""
    You are a professional career coach. Write a highly tailored, persuasive job application letter.
    
    USER RESUME CONTENT:
    {st.session_state.resume_description}
    
    JOB DESCRIPTION:
    {st.session_state.position_description}

    HELPFUL CONVERSATION:
    {st.session_state.messages}
    
    INSTRUCTIONS:
    - Use a professional formal letter typst format as I provided ```{typst_content}´´´.
    - Match the user's skills specifically to the job requirements as I provided ```{tone_setting}´´´.
    - Return ONLY the content of the rewrite typst format.
    """
    
    with st.spinner("Writing application..."):
        try:
            response = client.chat.completions.create(
                model=st.session_state.selected_model,
                messages=[{"role": "user", "content": prompt}],
            )
            application_text = response.choices[0].message.content

            # 2. Display and Download
            st.success("Application Drafted Successfully!")
            
            # Show a preview in the app
            with st.expander("Preview Application"):
                st.text(application_text)

            # Streamlit handles the .txt generation internally when you pass a string
            st.download_button(
                label="Download as Text File",
                data=application_text,
                file_name="Job_Application.txt",
                mime="text/plain"
            )

        except Exception as e:
            st.error(f"An error occurred: {e}")



    
