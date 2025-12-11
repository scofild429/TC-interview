import streamlit as st
import time


def get_msg_placeholder():
    """
    Get or create the message placeholder that persists across reruns.
    The placeholder must be created at the top of the app to always be visible.
    """
    if "msg_placeholder" not in st.session_state:
        st.session_state.msg_placeholder = st.empty()
    return st.session_state.msg_placeholder


def display_notification():
    """
    Check if there's a notification to display and show it.
    This should be called at the beginning of the app after creating the placeholder.
    """

    get_msg_placeholder()

    if st.session_state.notification_message_content:
        msg_placeholder = get_msg_placeholder()
        msg_placeholder.success(st.session_state.notification_message_content)

        # Sleep to show the notification
        time.sleep(st.session_state.notification_message_time)

        # Clear the notification
        msg_placeholder.empty()
        st.session_state.notification_message_content = None
        st.session_state.notification_message_time = 0


def show_notificaton_message(message, duration):
    """
    Set a notification message to be displayed at the top of the app.

    Args:
        message: The message to display
        duration: How long to display the message (in seconds)
    """
    st.session_state.notification_message_content = message
    st.session_state.notification_message_time = duration
    st.rerun()


def show_message_callback(message, duration):
    """
    Display a success message immediately at the top of the app.

    Args:
        message: The success message to display
        duration: How long to display the message (in seconds)
    """
    msg_placeholder = get_msg_placeholder()

    msg_placeholder.success(message)
    # This pauses execution so the user can see the popup
    time.sleep(duration)
    # Clear the message
    msg_placeholder.empty()
