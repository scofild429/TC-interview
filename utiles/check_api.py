import streamlit as st
from openai import OpenAI, AuthenticationError, APIConnectionError, RateLimitError
from .notifications import show_message_callback


def check_api_key():
    
    api_key = st.session_state.api_key
    
    if not api_key:
        return
    check_api_key_function(api_key)

    
def check_api_key_function(api_key):
    if not api_key.startswith("sk-"):
        st.warning("Invilid: ONLY OPENAI API Key allowed!")
    else:
        try:
            with st.spinner("Validating API Key..."):
                client = OpenAI(api_key = api_key)
                response =  client.models.list()
                
                available_model = []
                for item in response:
                    available_model.append(item.id)

                st.session_state.api_key = api_key
                st.session_state.available_model = available_model
                st.session_state.config_toggle = False
                show_message_callback("Login Successful! Redirecting...", 2)

        except AuthenticationError:
            st.error("Authentication Failed: Incorrect API Key.")
        except APIConnectionError:
            st.error("Connection Error: Unable to reach OpenAI. Check your internet.")
        except RateLimitError:
            st.error("Quota Exceeded: Your key is valid, but you have no credits left.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
