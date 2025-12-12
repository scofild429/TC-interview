"""
Notification and messaging system for user feedback.

This module provides a centralized notification system that:
- Creates persistent message placeholders at the top of the app
- Displays success messages with auto-dismissal
- Handles notification timing and cleanup
- Works across Streamlit reruns
"""

import streamlit as st
import time


def get_msg_placeholder():
    """
    Get or create the message placeholder that persists across reruns.
    
    The placeholder is stored in session state to maintain its position
    at the top of the app across reruns. This ensures notifications
    always appear in a consistent, visible location.
    
    Returns:
        streamlit.delta_generator.DeltaGenerator: Message placeholder
    """
    if "msg_placeholder" not in st.session_state:
        st.session_state.msg_placeholder = st.empty()
    return st.session_state.msg_placeholder


def display_notification():
    """
    Check and display any pending notifications at app startup.
    
    This function should be called at the beginning of the main app file
    (after session initialization but before other UI elements).
    
    If a notification is pending (notification_message_content is set):
    1. Displays the success message
    2. Pauses for the specified duration
    3. Clears the message and resets the notification state
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
    Queue a notification message for display and trigger app rerun.
    
    This function stores the message in session state and triggers
    a rerun. On the next render, display_notification() will show
    the message at the top of the app.
    
    Args:
        message (str): The notification message to display
        duration (int/float): How long to display the message (in seconds)
    
    Note: Triggers st.rerun() to immediately show the notification
    """
    st.session_state.notification_message_content = message
    st.session_state.notification_message_time = duration
    st.rerun()


def show_message_callback(message, duration):
    """
    Display a success message immediately without rerunning.
    
    Unlike show_notificaton_message(), this function displays the
    message synchronously without triggering a rerun. Useful for
    showing messages within callback functions or during operations
    where a rerun would be disruptive.
    
    Args:
        message (str): The success message to display
        duration (int/float): How long to display the message (in seconds)
    """
    msg_placeholder = get_msg_placeholder()

    msg_placeholder.success(message)
    # This pauses execution so the user can see the popup
    time.sleep(duration)
    # Clear the message
    msg_placeholder.empty()
