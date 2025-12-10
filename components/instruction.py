import streamlit as st
import PyPDF2
from utiles.notifications import show_notificaton_message
from .action import toggel_review_pdf_content, toggle_review_url_content, action_llm_phase_url, llm_phase_url, phase_pdf


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
        height=300,
        key="selected_prompt_content",
        help="Type your text and click away (or Ctrl+Enter) to save."
    )    

    
def input_url():
    col1, col2 = st.columns([9, 1])
    with col1:
        st.text_input(
            "You can provide the position URL",
            key="input_url",
            on_change=action_llm_phase_url,
            placeholder="Position URL, start with http"
        )
    with col2:
        st.button("View URL Content", on_click = toggle_review_url_content)

    if st.session_state.review_url_content:
        with st.container(height=500):
            if st.session_state.position_description:
                st.markdown(st.session_state.position_description)
            else:
                st.write("Analysis this URL at first.")
            

def resume_input():
    col1, col2 = st.columns([9, 1])
    with col1:
        upload_pdf = st.file_uploader(
            "You can load your resume as PDF",
            label_visibility="collapsed",
            on_change = phase_pdf,
            type="pdf"
        )
        
        #        print(st.session_state.toggle_input_pdf)
        if st.session_state.toggle_input_pdf:
            st.session_state.toggle_input_pdf = False
            if upload_pdf is not None:
                pdf_reader = PyPDF2.PdfReader(upload_pdf)
                pdf_content = ""
                for page in pdf_reader.pages:
                    pdf_content += page.extract_text() + "\n"
                st.session_state.resume_description = pdf_content
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


def review_url():
    if st.session_state.action_llm_phase_url:
        st.session_state.action_llm_phase_url = False
        llm_phase_url()

        
