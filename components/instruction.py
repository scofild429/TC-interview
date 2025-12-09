import streamlit as st
import requests
import textwrap
import PyPDF2
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from utiles.llm_model import url_input_analysis
from utiles.notifications import show_notificaton_message
from openai import OpenAI


def input_system_instruction():
    st.header("You are prepare now a interview!")
    st.text_area(
        "System instruction with selected prompt",
        height=120,
        key="system_instruction",
        value = "You are a great assistant, I want you help me to prepare an interview.",
        help="Type your text and click away (or Ctrl+Enter) to save."
    )

def input_selected_prompt():
    st.text_area(
        "You selected prompt",
        height=100,
        key="selected_prompt_content",
        help="Type your text and click away (or Ctrl+Enter) to save."
    )    

def input_url():
    url_input = ""
    url_context = ""
    col1, col2 = st.columns([8, 2])
    with col1:
        url_input = st.text_input(
            "You can provide the position URL",
            label_visibility="collapsed",
            placeholder="Position URL, start with http"
        )
        if url_input:
            if not url_input.startswith("http"):
                st.error("Your URL should starts with 'http' or 'https'")
            else:
                try:
                    with st.spinner(f"Querying {url_input}"):
                        #time out check
                        response = requests.get(url_input, timeout=5)
                        response.raise_for_status()
                        url_context = response.text

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

    with col2:
        if st.button("Analysis the URL"):
            if url_input == "" or st.session_state.select_model is None:
                show_notificaton_message("please make sure you input valided URL and set the API key already", 2)
            else:
                extract_content = url_input_analysis(url_context)
                st.session_state.position_description = extract_content
                with st.container(height=500):
                    st.markdown(textwrap.dedent(str(st.write_stream(extract_content))))
                

def resume_input():
    pdf_reader = None
    
    col1, col2 = st.columns([8, 2])
    with col1:
        upload_pdf = st.file_uploader(
            "You can load your resume as PDF",
            label_visibility="collapsed",
            type="pdf"
        )
        if upload_pdf is not None:
            pdf_reader = PyPDF2.PdfReader(upload_pdf)        
    with col2:
        if st.button("Phasing this PDF resume"):
            if pdf_reader is not None:
                pdf_content = ""
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"
                st.session_state.resume_description = pdf_content
                show_notificaton_message("PDF is successful phased.", 2)
            else:
                show_notificaton_message("You PDF has no contxt", 2)

    
                
def input_zero_shut_prompt():
    st.divider()

    col1, col2 = st.columns([8, 2])
    prompt = ""
    with col1:
        zero_shut_prompt = st.text_area(
            "Zero shut Prompt",
            height=120,
            value = "I want you give me some advance.",
            help="change your input prompt as you like."
        )
        prompt =  f"Given the materials: ```{st.session_state.position_description }, { st.session_state.resume_description }```, {zero_shut_prompt}"
    with col2:
        if st.button("Try zero shut prompt"):
            if st.session_state.select_model is None:
                show_notificaton_message("please make sure you input valided URL and set the API key already", 2)
            else:
                client = OpenAI(api_key = st.session_state.api_key)
                response = client.chat.completions.create(
                    model = st.session_state.select_model,
                    messages = [
                        {"role": "system", "content": st.session_state.system_instruction },
                        {"role": "user", "content": prompt}
                    ]
                )
                
    
 
