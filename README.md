# Prompt Versioning

A Streamlit application for managing prompt versions, running A/B experiments, and comparing response results from Gemini.

## Requirements

- Python 3.14 or compatible Python version
- MySQL 8.0 running locally
- A Gemini API key

## Setup

Open PowerShell in the project directory:

```powershell
cd "C:\Users\sahan\OneDrive\Desktop\Prompt-Versioning"

.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit `.env` and provide your real values:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password_here
DB_NAME=prompt_project_db
```

Never commit `.env` or place real credentials in `.env.example`.

## Initialize MySQL

Create the database tables with the MySQL client:

```powershell
& "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe" -h localhost -P 3306 -u root -p < db\schema.sql
```

The schema creates these tables:

- `prompts`
- `prompt_versions`
- `experiments`
- `results`

## Run the application

```powershell
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

Open the URL shown by Streamlit, usually `http://localhost:8501`.

## How to use it

1. Open **1. Prompts** and create a prompt.
2. Add at least two prompt versions. Include `{input}` where user input should be inserted.
3. Open **2. Experiments**, select the prompt and two different versions, then start an experiment.
4. Open **3. Run & Test**, submit test inputs, and record responses through the router.
5. Open **4. Dashboard** to compare average scores, p-values, and raw results.

The router assigns a browser session consistently to Version A or Version B, which keeps the experiment assignment stable for that session.

## Tests

Run the routing sanity check:

```powershell
.\venv\Scripts\python.exe test_routing.py
```

Compile the project files:

```powershell
.\venv\Scripts\python.exe -m py_compile evaluation.py experiments.py llm_client.py routing.py stats_utils.py streamlit_app.py versioning.py db\connection.py
```
