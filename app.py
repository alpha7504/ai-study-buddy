import streamlit as st
import requests
import json


st.title("AI-Powered Study Buddy")
st.write("Enter a topic, notes, or question, and get explanations, summaries, or quizzes!")


API_KEY = st.secrets["GEMINI_API_KEY"] 

def get_ai_response(prompt):

    # safer free-tier model
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

    headers = {"Content-Type": "application/json"}

    # limit token usage (VERY IMPORTANT)
    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ],
        "generationConfig": {
            "maxOutputTokens": 200,
            "temperature": 0.6
        }
    }

    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)

        if response.status_code == 200:
            result = response.json()
            return result["candidates"][0]["content"]["parts"][0]["text"]

        elif response.status_code == 429:
            return "⚠️ AI usage limit reached temporarily. Please try again later."

        else:
            return f"API Error {response.status_code}"

    except requests.exceptions.Timeout:
        return "⚠️ AI response timed out. Please retry."

    except Exception:
        return "⚠️ Something went wrong while contacting AI service."


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
