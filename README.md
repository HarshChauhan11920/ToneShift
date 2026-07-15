# ToneShift

ToneShift is a Streamlit app that rewrites text for different audiences and checks whether the rewrite preserved the original meaning.

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
