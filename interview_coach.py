import streamlit as st
import requests
import json

# Ollama Base URL
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"  # Ensure Ollama is running

# Function to generate an interview question from Ollama
def get_interview_question(job_role, question_type, difficulty_level):
    prompt = f"""
    You are an AI interview coach.
    Generate a short and concise {question_type} interview question for a {job_role} role.
    The difficulty level is {difficulty_level}. 
    Only return the question itself without extra text.
    """

    payload = {
        "model": "llama3.2",  # Updated to use Llama 3.2
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

# Streamlit UI
st.title("🎯 AI Interview Coach")

# Input Fields
job_role = st.text_input("Enter Job Role (e.g., Data Scientist, Software Engineer):")
question_type = st.selectbox("Select Type of Question:", ["Technical", "Behavioral"])
difficulty_level = st.selectbox("Select Difficulty Level:", ["Beginner", "Intermediate", "Expert"])

# Generate Button
if st.button("Generate Interview Question"):
    if job_role.strip():  # Ensures job role is not empty
        with st.spinner("Generating question..."):
            question = get_interview_question(job_role, question_type, difficulty_level)
        st.subheader("Generated Interview Question:")
        st.write(question)
    else:
        st.warning("Please enter a job role before generating a question.")
