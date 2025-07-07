# app.py

import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load your API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client (new style for >=1.0.0 SDK)
client = OpenAI(api_key=api_key)

# Streamlit setup
st.set_page_config(page_title="AI Prompt Enhancer", layout="centered")
st.title("🧠 AI Prompt Enhancer")

# Input fields
role = st.text_input("Enter the Role")
context = st.text_area("Enter the Context")
task = st.text_area("Enter the Task")

# Optional debug info
if role or context or task:
    st.write("🔍 Debug Info:", {"Role": role, "Context": context, "Task": task})

# Button handler
if st.button("Enhance Prompt"):
    if not api_key:
        st.error("❌ OpenAI API key not found. Please check your .env file.")
    elif role and context and task:
        with st.spinner("Enhancing your prompt..."):
            user_prompt = f"""
Given the following inputs:

Role: {role}
Context: {context}
Task: {task}

Write an improved version of a prompt that:
1. Is clear and specific
2. Asks GPT to clarify assumptions before responding
3. Specifies the expected format of the output
"""
            try:
                # Use the new client.chat.completions.create() interface
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system",
                         "content": "You are a helpful AI assistant that improves prompts for GPT-based tools."},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.7
                )
                enhanced_prompt = response.choices[0].message.content
                st.subheader("🔧 Enhanced Prompt")
                st.code(enhanced_prompt, language="markdown")

            except Exception as e:
                st.error(f"❌ OpenAI API error: {e}")
    else:
        st.warning("⚠️ Please fill in all the inputs: Role, Context, and Task.")
