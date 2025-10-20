# Torii Project (Security Toolkit)

[![CI](https://github.com/paladuguganeshnaidu/paladuguganesh/actions/workflows/ci.yml/badge.svg)](https://github.com/paladuguganeshnaidu/paladuguganesh/actions/workflows/ci.yml)

A lightweight security toolbox with a Flask backend and a static frontend.

Includes tool stubs for:
- Email Analyzer, URL Scanner, Password Cracker, SMS Spam Tester, Malware Analyzer, Web Recon
- Steganography checker (frontend page + backend API)

## Quick start (Windows PowerShell)

Backend (Flask):

```powershell
cd C:\python\Torii-Project\Backend
py -3 -m venv .venv
 .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

Frontend:
- Option 1 (static): open `frontend/index.html` with VS Code Live Server (port 5500)
- Option 2 (server-rendered): visit http://127.0.0.1:5000/ and use `/tool/<name>` routes

Steganography Tool 7 (frontend page):
- File: `frontend/tool7-steganography-checker.html`
- When opened via Live Server, it will send requests to `http://127.0.0.1:5000/api/detect_stego`.

## API docs
See `docs/api-documentation.md` for the current `/api/*` endpoints, parameters, and responses.

## Logging
Backend logs are written to `logs/app.log` with rotation (max ~1MB, 5 backups). Requests are logged via `@app.before_request`.

## Testing
Install test deps and run pytest:

```powershell
cd C:\python\Torii-Project
py -3 -m venv .venv
 .\.venv\Scripts\Activate.ps1
pip install -r Backend\requirements.txt pytest requests
pytest
```

Notes:
- API smoke tests auto-skip if the Flask server is not running locally.

## Environment
Copy `.env.example` to `.env` (optional) and adjust:

```
FLASK_ENV=development
TORII_SECRET=change-me
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000
```

## Project structure (excerpt)

```
Torii-Project/
├─ Backend/
│  ├─ app.py                 # Flask app, routes + API
│  ├─ auth.py                # Auth blueprint (skeleton)
│  ├─ tools/                 # Tool modules
│  ├─ templates/             # Jinja templates
│  ├─ utils/                 # Backend helpers
│  └─ requirements.txt
├─ frontend/
│  ├─ index.html             # Static homepage
│  ├─ tool7-steganography-checker.html
│  ├─ css/, js/, assets/, templates/
├─ docs/                     # API + user + dev docs
├─ tests/                    # Pytest smoke tests
├─ logs/                     # Rotating logs
├─ .github/workflows/ci.yml  # CI: run tests on push
└─ .env.example, .gitignore
```

## CI
A GitHub Actions workflow runs `pytest` on pushes to `main`. The API smoke tests are skipped automatically if the backend is not running in CI.

## Contributing / pushing changes

```powershell
git add .
git commit -m "feat: update docs and wire components"
git push
```

Repository: https://github.com/paladuguganeshnaidu/paladuguganesh

