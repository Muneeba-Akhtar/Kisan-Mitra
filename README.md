# Kisan Mitra (किसान मित्र)

A simple agricultural-advisory hackathon prototype with a responsive HTML/CSS/JavaScript frontend and a Python Flask backend.

## Project files
- `index.html` — website UI and browser-side fallback demo.
- `app.py` — Flask backend with the `POST /api/advice` rule-based endpoint.
- `requirements.txt` — Python packages needed to run/deploy the backend.
- `.gitignore` — prevents Python cache, virtual environments, and local secrets from being committed.
- `.env.example` — example placeholder only; no API key is needed for the current demo.

## Run locally in VS Code
1. Install Python 3.10 or newer.
2. Open this folder in VS Code.
3. Open the VS Code terminal in this folder.
4. (Recommended) Create a virtual environment:
   - Windows: `py -m venv .venv`
   - Activate it in PowerShell: `.venv\\Scripts\\Activate.ps1`
5. Install dependencies: `python -m pip install -r requirements.txt`
6. Start the website and backend: `python app.py`
7. Open `http://127.0.0.1:5000` in your browser.

## Deploy the website + backend on Render
1. Push all project files to a GitHub repository.
2. In Render, create a **New Web Service** and connect the repository.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn app:app`
5. Deploy. Render will provide a URL serving both the website and the `/api/advice` endpoint.

## Important limitations
This is a rule-based demo, not a live Gemma/Gemini model. It does not fetch live weather or retrieve verified agricultural documents. Treat responses as general prototype guidance, not a diagnosis or pesticide prescription. Confirm crop-specific treatment with a local Krishi Vigyan Kendra (KVK) or agriculture officer.

GitHub Pages hosts static files only and cannot run the Python backend. For a working online backend, deploy the repository as a Render Web Service.
