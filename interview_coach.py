import streamlit as st
import requests
import json


OLLAMA_BASE_URL = "http://localhost:11434/api/generate"  


def get_interview_question(job_role, question_type, difficulty_level):
    prompt = f"""
    You are an AI interview coach.
    Generate a short and concise {question_type} interview question for a {job_role} role.
    The difficulty level is {difficulty_level}. 
    Only return the question itself without extra text.
    """

    payload = {
        "model": "llama3.2",  
        "prompt": prompt,
        "stream": False
    }

    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(OLLAMA_BASE_URL, data=json.dumps(payload), headers=headers)
        if response.status_code == 200:
            return response.json().get("response", "No response generated.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"


st.title("🎯 AI Interview Coach")

# Input Fields
job_role = st.text_input("Enter Job Role (e.g., Data Scientist, Software Engineer):")
question_type = st.selectbox("Select Type of Question:", ["Technical", "Behavioral"])
difficulty_level = st.selectbox("Select Difficulty Level:", ["Beginner", "Intermediate", "Expert"])


if st.button("Generate Interview Question"):
    if job_role.strip():  
        with st.spinner("Generating question..."):
            question = get_interview_question(job_role, question_type, difficulty_level)
        st.subheader("Generated Interview Question:")
        st.write(question)
    else:
        st.warning("Please enter a job role before generating a question.")
