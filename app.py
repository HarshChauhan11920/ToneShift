import streamlit as st
from dotenv import load_dotenv
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

load_dotenv()

st.set_page_config(
    page_title="ToneShift",
    page_icon="🎭",
    layout="wide"
)

from config.settings import SIMILARITY_THRESHOLD
from core.back_translation import back_translate
from core.prompt_builder import build_prompt
from core.rewriter import rewrite_text
from core.similarity import meaning_drift, similarity_score
from utils.diff_highlighter import highlight_differences


# image loader
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

dark_bg = get_base64_image("images/black_bg.avif")
light_bg = get_base64_image("images/white_bg.avif")

# pdf generator
def create_pdf(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)

    text_object = pdf.beginText(50, 800)
    text_object.setFont("Helvetica", 12)

    for line in text.splitlines():
        text_object.textLine(line)

    pdf.drawText(text_object)
    pdf.save()

    return buffer.getvalue()

# =========================
# 🌗 THEME STATE
# =========================
if "theme" not in st.session_state:
    st.session_state.theme = "dark"

def toggle_theme():
    st.session_state.theme = "light" if st.session_state.theme == "dark" else "dark"


# =========================
# 🎨 ADVANCED UI CSS
# =========================
st.markdown(f"""
<style>

/* ===== BACKGROUND ===== */
.stApp {{
    background: url("data:image/avif;base64,{dark_bg if st.session_state.theme == "dark" else light_bg}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}}

/* REMOVE pattern overlay */
.stApp::before {{
    content: "";
    display: none;
}}

/* container */
.block-container {{
    position: relative;
    z-index: 1;
    padding-top: 2rem;
}}

/* sidebar glass */
section[data-testid="stSidebar"] {{
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(255,255,255,0.1);
}}

/* text colors */
h1, h2, h3, h4, h5, h6, p, span, label {{
    color: {"#ffffff" if st.session_state.theme == "dark" else "#000000"} !important;
}}

/* textarea */
textarea {{
    background: rgba(255,255,255,0.08) !important;
    color: {"white" if st.session_state.theme == "dark" else "black"} !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}}

/* buttons */
.stButton>button {{
    border-radius: 12px;
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    color: white;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
    transition: 0.3s;
}}

.stButton>button:hover {{
    transform: scale(1.05);
    box-shadow: 0 6px 20px rgba(0,0,0,0.4);
}}

/* metrics */
[data-testid="stMetric"] {{
    background: rgba(255,255,255,0.08);
    padding: 1rem;
    border-radius: 12px;
}}

</style>
""", unsafe_allow_html=True)


# =========================
# 🎭 HEADER
# =========================
col1, col2 = st.columns([8,1])

with col1:
    st.title("🎭 ToneShift")
    st.caption("Audience-aware rewriting with meaning preservation")

with col2:
    st.button("🌗", on_click=toggle_theme)

st.divider()


# =========================
# ⚙️ SIDEBAR
# =========================
with st.sidebar:
    st.header("⚙️ Controls")

    tone = st.selectbox(
        "Tone",
        ["Formal", "Casual", "Child-friendly", "Executive Summary"],
    )

    audience = st.selectbox(
        "Audience",
        ["General", "Students", "Professionals", "Children"],
    )

    formality = st.slider("Formality", 1, 10, 5)
    length = st.slider("Length", 1, 10, 5)

    include_analysis = st.checkbox("Enable Meaning Analysis", value=True)

    st.divider()
    st.caption("Built with ❤️ using Streamlit + LLMs")


# =========================
# 📝 INPUT
# =========================
st.markdown('<div class="glass">', unsafe_allow_html=True)

st.subheader("📝 Input Text")

input_text = st.text_area(
    "",
    height=180,
    placeholder="Paste your text here..."
)

rewrite_clicked = st.button("✨ Rewrite")

st.markdown('</div>', unsafe_allow_html=True)


# =========================
# 🚀 PROCESS
# =========================
if rewrite_clicked:
    if not input_text.strip():
        st.warning("⚠️ Please enter some text.")
    else:
        with st.spinner("✨ Rewriting... please wait"):
            try:
                prompt = build_prompt(input_text, tone, audience, formality, length)
                rewritten_text = rewrite_text(prompt)

                st.divider()

                tab1, tab2, tab3 = st.tabs(["✨ Rewrite", "🔍 Differences", "🧠 Analysis"])

                # =========================
                # ✨ OUTPUT
                # =========================
                with tab1:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown('<div class="glass">', unsafe_allow_html=True)
                        st.subheader("📄 Original")
                        st.write(input_text)
                        st.markdown('</div>', unsafe_allow_html=True)

                    with col2:
                        st.markdown('<div class="glass">', unsafe_allow_html=True)
                        st.subheader(f"✨ Rewritten ({tone})")
                        st.write(rewritten_text)
                        st.markdown('</div>', unsafe_allow_html=True)

                    colA, colB = st.columns(2)

                    with colA:
                        pdf_data = create_pdf(rewritten_text)

                        st.download_button(
                            "⬇️ Download PDF",
                            data=pdf_data,
                            file_name="rewritten.pdf",
                            mime="application/pdf",
                        )
                    with colB:
                        st.button("📋 Copy (Ctrl+C)")

                # =========================
                # 🔍 DIFF
                # =========================
                with tab2:
                    st.markdown('<div class="glass">', unsafe_allow_html=True)
                    st.subheader("🔍 Differences")
                    diff_html = highlight_differences(input_text, rewritten_text)
                    st.markdown(diff_html, unsafe_allow_html=True)
                    st.markdown('</div>', unsafe_allow_html=True)

                # =========================
                # 🧠 ANALYSIS
                # =========================
                with tab3:
                    if include_analysis:
                        back_text = back_translate(rewritten_text)
                        score = similarity_score(input_text, back_text)

                        col3, col4 = st.columns(2)

                        with col3:
                            st.markdown('<div class="glass">', unsafe_allow_html=True)
                            st.subheader("🔁 Back Translation")
                            st.write(back_text)
                            st.markdown('</div>', unsafe_allow_html=True)

                        with col4:
                            st.markdown('<div class="glass">', unsafe_allow_html=True)
                            st.subheader("📊 Similarity")

                            st.metric("Score", f"{score:.2f}")

                            if not meaning_drift(score, SIMILARITY_THRESHOLD + 0.9):
                                st.success("Excellent preservation")
                                st.progress(95)
                            elif not meaning_drift(score, SIMILARITY_THRESHOLD):
                                st.warning("Minor drift")
                                st.progress(75)
                            else:
                                st.error("Meaning changed significantly")
                                st.progress(40)

                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.info("Enable analysis from sidebar to view insights.")

            except Exception as exc:
                error_message = str(exc).lower()

                if "quota" in error_message:
                    st.error("🚫 API quota exceeded. Check billing.")
                elif "api_key" in error_message:
                    st.error("🔑 Missing API key in .env file.")
                else:
                    st.error(f"❌ Error: {exc}")
