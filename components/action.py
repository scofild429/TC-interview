import streamlit as st
from io import StringIO
from utiles.llm_model import initial_llm_model
import requests
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from .variables import assemble_prompt_content


def change_prompt_strategy():
    assemble_prompt_content()
    if st.session_state.selected_prompt_strategy is not None:
        for strategy, content in st.session_state.prompt_strategies[
            ["strategy", "content"]
        ].values:
            if st.session_state.selected_prompt_strategy == strategy:
                st.session_state.selected_prompt_content = content

    
def toggle_review_url_content():
    st.session_state.review_url_content = not st.session_state.review_url_content
    
def toggel_review_pdf_content():
    st.session_state.review_pdf_content = not st.session_state.review_pdf_content

def action_llm_phase_url():
    st.session_state.action_llm_phase_url = True

def llm_phase_url():
    url_input = st.session_state.input_url
    if url_input:
        if not url_input.startswith("http"):
            st.error("Your URL should starts with 'http' or 'https'")
        else:
            try:
                with st.spinner(f"Querying {url_input}"):
                    response = requests.get(url_input, timeout=5)
                    response.raise_for_status()

                    client = initial_llm_model()
                    if client is None:
                        return None

                    response = client.chat.completions.create(
                        model = st.session_state.selected_model,
                        messages = [
                            {"role": "system", "content": "You are a very helpful assistant, please extract the complete position informatoin, without any imgaes included, and then convert it into markdown format, please be careful and think hard, you have to return valid markdown format."},
                            {"role": "user", "content": response.text}
                        ],
                        stream = True
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
                st.error(f"❌ HTTP Error: The server returned code{http_err.response.status_code}")
                st.code(str(http_err), language="bash")

            except ConnectionError:
                # Handles DNS failures or refused connections
                st.error("❌ Connection Error: Could not reach the server.")

            except Timeout:
                # Handles cases where the server is too slow
                st.error("❌ Timeout: The server took too long to respond (>5 seconds).")

            except RequestException as e:
                # Catch-all for any other weird requests-related errors
                st.error(f"❌ An unexpected error occurred: {e}")            


def phase_pdf():
    st.session_state.toggle_input_pdf =  True
