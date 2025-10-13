import streamlit as st
import requests
import json


st.title("AI-Powered Study Buddy")
st.write("Enter a topic, notes, or question, and get explanations, summaries, or quizzes!")


API_KEY = st.secrets["GEMINI_API_KEY"] 

def get_ai_response(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        return f"Error: {response.status_code} - {response.text}"


user_input = st.text_area("Enter your topic or study notes:")


mode = st.radio(
    "Choose what you want the AI to do:",
    ["Explain", "Summarize", "Generate Quiz", "Create Flashcards"]
)


if st.button("Ask AI"):
    if user_input.strip() == "":
        st.warning("Please type something first.")
    else:
        st.write("🤖 Thinking...")

        
        if mode == "Explain":
            prompt = f"Explain the following topic in simple terms for a student:\n\n{user_input}"
        elif mode == "Summarize":
            prompt = f"Summarize the following study notes clearly and briefly in 5 points:\n\n{user_input}"
        elif mode == "Generate Quiz":
            prompt = f"Create 5 short quiz questions and answers for the following topic:\n\n{user_input}"
        elif mode == "Create Flashcards":
            prompt = f"Make 5 flashcards (Question: Answer format) for the following topic:\n\n{user_input}"

       
        answer = get_ai_response(prompt)
        st.subheader("AI Response:")
        st.write(answer)