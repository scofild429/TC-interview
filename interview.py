import streamlit as st
from utiles.notifications import  display_notification, show_notificaton_message
from components.init import initial_session
from components.sidebar import initial_sidebar
from components.instruction import input_system_instruction, input_url, resume_input, input_selected_prompt, review_url
from utiles.llm_model import initial_llm_model
from openai.types.chat import ChatCompletionMessageParam


initial_session()

st.set_page_config(
    page_title="Interview",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.config_toggle else "collapsed"
)

# Check and display any pending notifications
display_notification()

initial_sidebar()


input_url()
review_url()

resume_input()

input_system_instruction()
input_selected_prompt()



for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Input or Enter your start... "):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)


    messages: list[ChatCompletionMessageParam] = [{"role": "system", "content": f"{st.session_state.system_instruction}{st.session_state.selected_prompt_content}"}]
    for m in st.session_state.messages:
        messages.append({"role": m["role"], "content": m["content"]})
    
    with st.chat_message("assistant"):
        if client := initial_llm_model():        
            stream = client.chat.completions.create(
                model = st.session_state.selected_model,
                messages = messages,
                stream=True,
            )
            response = st.write_stream(stream)
            st.session_state.messages.append({"role": "assistant", "content": response})
        else:
            show_notificaton_message("Model can't be initialized, please check the API key", 2 )



