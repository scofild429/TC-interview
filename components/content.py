"""
User input components for the interview preparation interface.

This module provides UI components for:
- System instruction input
- Job position URL input and display
- Resume PDF upload and text extraction
- Content review panels
"""

import streamlit as st
import PyPDF2
from utiles.show_notifications import show_notificaton_message
from utiles.actions import (
    toggel_review_pdf_content,
    toggle_review_url_content,
    toggle_llm_phase_url,
    llm_phase_url,
    parse_pdf, llm_parse_pdf,
)


def input_system_instruction():
    """
    Render the system instruction text area.

    This allows users to customize the base system prompt that guides
    the AI assistant's behavior. The default instruction sets up the AI
    as an interview preparation helper.
    """
    st.text_area(
        "System instruction with selected prompt",
        height=120,
        key="system_instruction",
        value="You are a great assistant, I want you help me to prepare an interview.",
        help="Type your text and click away (or Ctrl+Enter) to save.",
    )


def input_selected_prompt():
    """
    Render the selected prompt content display area.

    Shows the complete prompt that will be sent to the AI, combining
    the system instruction with the selected prompt strategy template.
    This is read-only and updates automatically when strategy changes.
    """
    st.text_area(
        "You selected prompt",
        height=300,
        key="selected_prompt_content",
        help="Type your text and click away (or Ctrl+Enter) to save.",
    )


def input_url_content():
    """
    Render the job position URL input component with review toggle.

    Provides:
    - Text input field for entering job posting URL
    - "View URL Content" button to toggle content display
    - Collapsible container showing extracted position description

    When URL changes, triggers LLM processing to extract job details.
    """
    col1, col2 = st.columns([8, 2])
    with col1:
        st.text_input(
            "You can provide the position URL",
            key="input_url",
            on_change=toggle_llm_phase_url,
            label_visibility="collapsed",
            placeholder="Position URL, start with http",
        )
    with col2:
        st.button("View URL Content", on_click=toggle_review_url_content)

    if st.session_state.review_url_content:
        with st.container(height=500):
            if st.session_state.position_description:
                st.markdown(st.session_state.position_description)
            else:
                st.write("Analysis this URL at first.")


def resume_input_content():
    """
    Render the resume PDF upload component with review toggle.

    Provides:
    - PDF file uploader
    - "View PDF Content" button to toggle content display
    - Collapsible container showing extracted resume text
    - PyPDF2-based text extraction

    Extracts text from all pages when PDF is uploaded and stores
    it in session state for use in prompt generation.
    """
    col1, col2 = st.columns([8, 2])
    with col1:
        upload_pdf = st.file_uploader(
            "You can load your resume as PDF",
            label_visibility="collapsed",
            on_change=parse_pdf,
            type="pdf",
        )

        #        print(st.session_state.toggle_input_pdf)
        if st.session_state.toggle_input_pdf:
            st.session_state.toggle_input_pdf = False
            if upload_pdf is not None:
                pdf_reader = PyPDF2.PdfReader(upload_pdf)
                pdf_content = ""
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"

                polisched_pdf_content = llm_parse_pdf(pdf_content)
                    
                st.session_state.resume_description = polisched_pdf_content
                show_notificaton_message("PDF is successful phased.", 2)
            else:
                show_notificaton_message("You PDF has no contxt", 2)
    with col2:
        st.button("View PDF Content", on_click=toggel_review_pdf_content)

    if st.session_state.review_pdf_content:
        with st.container(height=500):
            if st.session_state.resume_description:
                st.write(st.session_state.resume_description)
            else:
                st.write("Phasing the PDF at first.")


def review_url_extracted_content():
    """
    Process URL analysis when triggered by URL input change.

    This function checks if URL processing has been requested
    and calls llm_phase_url() to extract and format the job description.
    Resets the trigger flag after processing.
    """
    if st.session_state.action_llm_phase_url:
        st.session_state.action_llm_phase_url = False
        llm_phase_url()
