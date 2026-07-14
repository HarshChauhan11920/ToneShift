import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from core.prompt_builder import build_prompt

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Streamlit UI
st.set_page_config(page_title="ToneShift", layout="wide")

st.title("📝 ToneShift: Audience-Aware Rewriter")

# Input text
input_text = st.text_area("Enter your text:", height=200)

# Tone selection
tone = st.selectbox(
    "Select Tone:",
    ["Formal", "Casual", "Child-friendly", "Executive Summary"]
)

audience = st.selectbox(
    "Select Audience:",
    ["General", "Students", "Professionals", "Children"]
)

formality = st.slider("Formality Level", 1, 10, 5)

length = st.slider("Length Preference", 1, 10, 5)

# Button
if st.button("Rewrite Text"):

    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Rewriting..."):

            # Prompt
            prompt = build_prompt(
                input_text,
                tone,
                audience,
                formality,
                length
            )

            try:
                # LLM API Call
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a helpful text rewriter."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.7
                )

                rewritten_text = response.choices[0].message.content

                # Output
                st.subheader("Rewritten Text:")
                st.write(rewritten_text)

            except Exception as e:
                st.error(f"Error: {str(e)}")