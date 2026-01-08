"""
API key validation and authentication utilities.

This module handles:
- OpenAI API key validation
- API connection testing
- Available model retrieval
- Error handling for authentication issues
"""

import streamlit as st
from openai import AuthenticationError, APIConnectionError, RateLimitError
from .show_notifications import show_message_callback
from .llm_model import initial_llm_model


def check_api_key():
    """
    Callback function to validate API key from input field.

    Reads the API key from st.session_state.input_api_key and
    delegates validation to check_api_key_function().
    This is triggered by the on_change event of the API key input.
    """
    if api_key := st.session_state.input_api_key:
        check_api_key_function(api_key)
    else:
        return None


def check_api_key_function(api_key):
    """
    Validate OpenAI API key and fetch available models.

    Args:
        api_key (str): The OpenAI API key to validate

    Validation steps:
    1. Checks if key starts with "sk-" (OpenAI format)
    2. Attempts to create OpenAI client
    3. Fetches list of available models
    4. Stores API key and models in session state
    5. Switches to normal mode (config_toggle=False)

    Error handling:
    - AuthenticationError: Invalid API key
    - APIConnectionError: Network/connection issues
    - RateLimitError: Valid key but no credits
    - General exceptions: Other unexpected errors
    """
    if not api_key.startswith("sk-"):
        st.warning("Invilid: ONLY OPENAI API Key allowed!")
    else:
        st.session_state.api_key = api_key
        try:
            with st.spinner("Validating API Key..."):
                client = initial_llm_model()

                if client is None:
                    return None

                response = client.models.list()
                available_model = []
                for item in response:
                    if (
                        not item.id.endswith("instruct")  # remove legacy model
                        and "embedding" not in item.id.lower()  # remove embedding model
                        and "dall" not in item.id.lower()  # remove image generation model
                        and "tts" not in item.id.lower()  # remove text to speech model
                        and "whisper" not in item.id.lower()  # remove speech to text model
                    ):  # So sorry, this is no chat model specified in the model name(id)
                        available_model.append(item.id)

                #                st.session_state.api_key = api_key
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
