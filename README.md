# 🎭 ToneShift — Audience-Aware Text Rewriter

ToneShift is an intelligent text rewriting web app that adapts content based on **tone, audience, formality, and length**, while ensuring the **original meaning is preserved** using semantic analysis.

Built with **Streamlit + LLMs**, it provides a clean, interactive interface for transforming text in real time.

## Multilingual output

Choose an output language in the sidebar (English is the default). ToneShift rewrites the
text fully in that language, then translates the result back to neutral English and measures
semantic similarity against the original text. This keeps meaning-preservation checks useful
even when the rewritten text uses a different language or script.

---

## 🚀 Features

### ✨ Core Capabilities
- 🔁 Rewrite text into multiple tones:
  - Formal
  - Casual
  - Child-friendly
  - Executive Summary

- 🎯 Audience targeting:
  - General
  - Students
  - Professionals
  - Children

- 🎚️ Fine control:
  - Adjustable **formality level**
  - Adjustable **length preference**

---

### 🧠 Meaning Preservation Engine
- 🔁 **Back Translation** to verify semantic consistency  
- 📊 **Similarity Scoring** to measure meaning retention  
- 🚨 **Drift Detection**:
  - ✅ Excellent preservation  
  - ⚠️ Minor variation  
  - ❌ Significant meaning change  

---

### 🔍 Smart Diff Viewer
- Highlights exactly **what changed** between:
  - Original text
  - Rewritten version

---

### 🎨 Advanced UI/UX
- 🌗 Dark / Light theme toggle  
- 🧊 Glassmorphism UI (blur + transparency)  
- 🖼️ Dynamic background images (theme-based)  
- 📑 Tab-based layout:
  - Rewrite
  - Differences
  - Analysis  
- ⚡ Smooth interactions & loading states  

---

### 📦 Export & Utility
- ⬇️ Download rewritten text  
- 📋 Copy-ready output  
- ⚠️ Smart error handling (API, quota, config)

---

## 🏗️ Project Structure
ToneShift/
│
├── app.py # Main Streamlit app
│
├── core/
│ ├── prompt_builder.py # Builds LLM prompts
│ ├── rewriter.py # Calls LLM for rewriting
│ ├── back_translation.py # Neutral re-translation
│ └── similarity.py # Semantic similarity logic
│
├── utils/
│ └── diff_highlighter.py # Highlights text differences
│
├── config/
│ └── settings.py # Config constants
│
├── images/ # Background assets
│ ├── dark_bg.avif
│ └── light_bg.avif
│
├── .env # API keys
└── README.md


---

## ⚙️ How It Works

### Step-by-step pipeline:

1. **User Input**
   - Enter text
   - Select tone, output language, audience, formality, and length

2. **Prompt Generation**
   - `build_prompt()` constructs a structured instruction for the LLM

3. **Text Rewriting**
   - `rewrite_text()` generates the rewritten version

4. **Difference Analysis**
   - `highlight_differences()` shows word-level changes

5. **Meaning Validation (Optional)**
   - `back_translate()` converts rewritten text → neutral English
   - `semantic_similarity_score()` compares the original with the English back-translation
   - `meaning_drift()` flags inconsistencies

---

## 🛠️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/toneshift.git
cd toneshift

## Setup

Use a standard Windows Python install from python.org. The current `.venv` was created with MSYS Python, which can force packages such as NumPy to build from source. Rename or remove the existing `.venv` before recreating it.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Create a `.env` file with:

```text
GEMINI_API_KEY=your_api_key_here
```

Optional model overrides:

```text
GEMINI_MODEL=gemini-3.1-flash-lite
```

## Run

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```
