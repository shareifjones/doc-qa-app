# Document Q&A

A web app that lets you upload any text document and ask questions about it in plain English, powered by Claude AI.

## What it does
- Upload a .txt document
- Ask any question about its contents
- Get an accurate, formatted answer powered by Anthropic's Claude

## Tech stack
- Python
- Flask
- Anthropic Claude API

## How to run it
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Add your Anthropic API key to a `.env` file: `ANTHROPIC_API_KEY=your-key-here`
6. Run: `python3 web_app.py`