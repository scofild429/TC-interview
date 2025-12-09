import streamlit as st
from utiles.notifications import  display_notification
from components.init import initial_session
from components.sidebar import initial_sidebar
from components.instruction import input_system_instruction, input_url, resume_input, input_selected_prompt


initial_session()

st.set_page_config(
    page_title="Interview",
    layout="wide",
    initial_sidebar_state="expanded" if st.session_state.config_toggle else "collapsed"
)

# Check and display any pending notifications
display_notification()

initial_sidebar()

input_system_instruction()
input_selected_prompt()

input_url()

resume_input()


# st.title("AI helps your intevriew")
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# if "messages" not in st.session_state:
#     st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])


# if prompt := st.chat_input("What's up"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model="gpt-4.1-nano",
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )

#     response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})
