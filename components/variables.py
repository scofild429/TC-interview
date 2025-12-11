import streamlit as st
import pandas as pd


def init_prompt_content():
    standard_prompt_content = """
    You are a expert interview supporter, please help me to prepare my interview.
"""

    zero_shot_prompt_content = """
    You are a expert interview supporter, please help me to prepare my interview.
Please based on my information help me to generate a comprehensive interview preparation plan.
1. Analyze how well my skills match the job requirements.
2. tell me the toptics which I should concern and prepare.
3. Generate a few most likely technical questions and provide answer behind.
"""

    one_shot_prompt_content = """
    You are a expert interview supporter, please help me to prepare my interview.
Please based on my information help me to generate a comprehensive interview preparation plan.
1. Analyze how well my skills match the job requirements.
2. tell me the toptics which I should concern and prepare.
3. Generate a few most likely technical questions and provide answer behind.    

Example:
Job description requires Python experience and user resume has a few Python project listed.
Output: Your Python experience aligns well with the job requirements, especially since your resume includes several relevant Python projects. You should focus on preparing core Python concepts, data structures, and common libraries used in the role. Expect technical questions about your past Python projects, debugging scenarios, and how you structure clean, maintainable code. A likely question is: “Explain how you would optimize a slow Python script?”
"""

    few_shot_prompt_content = """
    You are a expert interview supporter, please help me to prepare my interview.
    Please based on my information help me to generate a comprehensive interview preparation plan.
1. Analyze how well my skills match the job requirements.
2. tell me the toptics which I should concern and prepare.
3. Generate a few most likely technical questions and provide answer behind.    

Example 1:
    Job description requires Python experience and user resume has a few Python project listed.
Output:
    Your Python experience aligns well with the job requirements, especially since your resume includes several relevant Python projects. You should focus on preparing core Python concepts, data structures, and common libraries used in the role. Expect technical questions about your past Python projects, debugging scenarios, and how you structure clean, maintainable code. A likely question is: “Explain how you would optimize a slow Python script?”

Example 2:
    Job description requires cloud infrastructure knowledge (AWS, CI/CD) and the user has DevOps and Linux experience.
Output:  
    Your background in Linux and DevOps aligns well with the cloud-focused requirements, especially if you’ve worked with automation or deployment workflows. You should prepare topics like AWS core services (EC2, S3, IAM), CI/CD pipelines, containerization, and monitoring. Expect questions about designing scalable cloud architectures and troubleshooting production issues. A likely question is: “How would you design a highly available deployment pipeline?”.
"""

    CoT_prompt_content = """
    You are a expert interview supporter, please help me to prepare my interview.
Please based on my information help me to generate a comprehensive interview preparation plan.
    Think: Make sure that you understand and jos description and user resume
1. Analyze how well my skills match the job requirements.
    Think: how to find the maximum common part and how to cover the gap
2. tell me the toptics which I should concern and prepare.
    Think: how to emphasize my strength
3. Generate a few most likely technical questions and provide answer behind.
    Think step by step how to provide a great answer

Example:
Job description requires Python experience and user resume has a few Python project listed.
Output: Your Python experience aligns well with the job requirements, especially since your resume includes several relevant Python projects. You should focus on preparing core Python concepts, data structures, and common libraries used in the role. Expect technical questions about your past Python projects, debugging scenarios, and how you structure clean, maintainable code. A likely question is: “Explain how you would optimize a slow Python script?”
    Think: if this question is related to the job description, and how to performance well to emphasise I am a perfect candidate.
"""

    delimiter_prompt_content = f"""
    You are a expert interview supporter, please help me to prepare my interview.
Please based on my information help me to generate a comprehensive interview preparation plan. The job description and resume descripton are  delimited by XML tags:
1. <position_description> {st.session_state.position_description}</position_description>
2. <resume_description>{st.session_state.resume_description}</resume_description>

1. Analyze how well my skills match the job requirements.
2. tell me the toptics which I should concern and prepare.
3. Generate a few most likely technical questions and provide answer behind.    

Example:
Job description requires Python experience and user resume has a few Python project listed.
Output: Your Python experience aligns well with the job requirements, especially since your resume includes several relevant Python projects. You should focus on preparing core Python concepts, data structures, and common libraries used in the role. Expect technical questions about your past Python projects, debugging scenarios, and how you structure clean, maintainable code. A likely question is: “Explain how you would optimize a slow Python script?”

"""
    return (
        standard_prompt_content,
        zero_shot_prompt_content,
        one_shot_prompt_content,
        few_shot_prompt_content,
        CoT_prompt_content,
        delimiter_prompt_content,
    )


def assemble_prompt_content():
    (
        standard_prompt_content,
        zero_shot_prompt_content,
        one_shot_prompt_content,
        few_shot_prompt_content,
        CoT_prompt_content,
        delimiter_prompt_content,
    ) = init_prompt_content()

    data = [
        {
            "strategy": "standard prompt ",
            "content": standard_prompt_content,
        },
        {
            "strategy": "zero shot prompt ",
            "content": zero_shot_prompt_content,
        },
        {
            "strategy": "one shot prompt",
            "content": one_shot_prompt_content,
        },
        {
            "strategy": "few shot prompt",
            "content": few_shot_prompt_content,
        },
        {
            "strategy": "Chain of Thought",
            "content": CoT_prompt_content,
        },
        {
            "strategy": "delimiter prompt",
            "content": delimiter_prompt_content,
        },
    ]
    st.session_state.prompt_strategies = pd.DataFrame(data)
