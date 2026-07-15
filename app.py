import streamlit as st
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="ToneShift", layout="wide")

from config.settings import SIMILARITY_THRESHOLD
from core.back_translation import back_translate
from core.prompt_builder import build_prompt
from core.rewriter import rewrite_text
from core.similarity import meaning_drift, similarity_score
from utils.diff_highlighter import highlight_differences


st.title("ToneShift: Audience-Aware Rewriter")

input_text = st.text_area("Enter your text:", height=200)

tone = st.selectbox(
    "Select Tone:",
    ["Formal", "Casual", "Child-friendly", "Executive Summary"],
)

audience = st.selectbox(
    "Select Audience:",
    ["General", "Students", "Professionals", "Children"],
)

formality = st.slider("Formality Level", 1, 10, 5)
length = st.slider("Length Preference", 1, 10, 5)
include_analysis = st.checkbox("Check meaning preservation", value=False)

if st.button("Rewrite Text"):
    if not input_text.strip():
        st.warning("Please enter some text.")
    else:
        with st.spinner("Processing..."):
            try:
                prompt = build_prompt(input_text, tone, audience, formality, length)
                rewritten_text = rewrite_text(prompt)

                st.divider()

                col1, col2 = st.columns(2)

                with col1:
                    st.subheader("Original Text")
                    st.write(input_text)

                with col2:
                    st.subheader(f"Rewritten ({tone})")
                    st.write(rewritten_text)

                st.download_button(
                    label="Download Rewritten Text",
                    data=rewritten_text,
                    file_name="rewritten.txt",
                    mime="text/plain",
                )

                st.subheader("What Changed")
                diff_html = highlight_differences(input_text, rewritten_text)
                st.markdown(diff_html, unsafe_allow_html=True)

                if include_analysis:
                    back_text = back_translate(rewritten_text)
                    score = similarity_score(input_text, back_text)

                    st.subheader("Back Translated Neutral Version")
                    st.write(back_text)

                    st.subheader("Meaning Similarity Score")
                    st.metric(label="Similarity", value=f"{score:.2f}")

                    if not meaning_drift(score, SIMILARITY_THRESHOLD + 0.9):
                        st.success("Excellent meaning preservation")
                    elif not meaning_drift(score, SIMILARITY_THRESHOLD):
                        st.warning("Minor meaning variation detected")
                    else:
                        st.error("Significant meaning drift detected")

            except Exception as exc:
                error_message = str(exc).lower()
                if "quota" in error_message or "resource_exhausted" in error_message:
                    st.error(
                        "Your Gemini API key has no available quota. Add billing/credits, "
                        "use another API key, or try again after your quota resets."
                    )
                elif "gemini_api_key" in error_message:
                    st.error("Add GEMINI_API_KEY to your .env file, then restart the app.")
                else:
                    st.error(f"Error: {exc}")
