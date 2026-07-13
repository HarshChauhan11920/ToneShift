import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

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

# Button
if st.button("Rewrite Text"):

    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Rewriting..."):

            # Prompt
            prompt = f"""
            Rewrite the following text in a {tone} tone.
            Preserve the original meaning. Do not add new information.

            Text:
            {input_text}
            """

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