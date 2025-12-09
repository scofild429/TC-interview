import streamlit as st

def change_prompt_strategy():
    if st.session_state.selected_prompt_strategy is not None:
        for strategy, content in st.session_state.prompt_strategies[
            ["strategy", "content"]
        ].values:
            if st.session_state.selected_prompt_strategy == strategy:
                st.session_state.selected_prompt_content = content
