# AI YouTube Video Analyzer

Analyze YouTube videos with an AI agent powered by Groq, Agno, and Streamlit. The app generates a structured report with topic flow, key moments, and useful timestamps.

## Features

- Analyze public YouTube videos from a simple web UI
- Generate structured video summaries with timestamped sections
- Validate YouTube URLs before processing
- Cache results for faster repeat analysis
- Download analysis as a Markdown report
- Deploy-ready Streamlit app with environment-based key management

## Tech Stack

- Python
- Streamlit
- Agno
- Groq API
- youtube-transcript-api

## Project Structure

```text
.
|-- ui.py
|-- ytVideoAnalyzer.py
|-- requirements.txt
|-- .env
```

## Prerequisites

- Python 3.10+
- A Groq API key

## Local Setup

1. Clone the repository:

```bash
git clone https://github.com/Official-Vinit/YoutubeVideoAnalyzer.git
```

2. Create and activate a virtual environment:

Windows (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

5. Start the app:

```bash
streamlit run ui.py
```

## How to Use

1. Open the Streamlit app in your browser.
2. Paste a valid YouTube video URL.
3. Click Analyze Video.
4. Review the generated report and optionally download it as a .md file.

## DEPLOYED ON STREAMLIT link:
<a href=https://ytvideoanalyzer.streamlit.app/>Click here</a>
