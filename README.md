# MigrationMatch

MigrationMatch is a Streamlit skill-to-city relocation platform. It helps blue-collar workers compare Indian cities using trade demand, salary, rent, savings, and quality-of-life indicators.

## Run locally (Windows)

Open PowerShell in this folder and run this single command:

```powershell
.\run_app.bat
```

The launcher creates `.venv` and installs the requirements the first time if needed, then starts Streamlit and opens the app in your browser. Keep the terminal window open while using the app; press `Ctrl+C` there to stop it.

## Run locally (manual)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app loads its dataset from `data/migrationmatch_dataset.csv`. Its SQLite database is created locally at `data/migrationmatch.db` and is intentionally excluded from Git.

## Project layout

```text
MigrationMatch/
├── app.py                 # Streamlit entry point and page routing
├── analysis/              # Data loading, cleaning, and exploration
├── data/                  # Dataset generator, CSV, and SQLite persistence code
├── model/                 # Recommendation and ML model logic
├── ui/                    # Shared UI, styles, session state, and pages/
├── assets/                # Static assets used by the interface
├── tests/                 # Automated tests
├── docs/                  # Project and contributor documentation
├── requirements.txt
├── run_app.bat            # One-command Windows launcher
└── .streamlit/            # Streamlit app configuration
```

Run `python -m data.generate_dataset` from any working directory to regenerate the CSV. Paths for the dataset and local database resolve from the project files rather than the shell's current directory.

`PHP PROJECT/` is a separate, unrelated project currently located beside the app; it is excluded from the MigrationMatch repository.

## Deploy with Streamlit Community Cloud

1. Push this project to a GitHub repository you own.
2. In Streamlit Community Cloud, create an app from that repository and select `app.py` as the entry point.
3. Add a private app secret before sharing the deployed app:

   ```toml
   admin_pin = "replace-with-a-long-unique-pin"
   ```

   Save this in the app's Streamlit secrets settings, not in the repository. Locally, the development PIN is `1234` unless overridden by the `MIGRATIONMATCH_ADMIN_PIN` environment variable.
4. Deploy the app. Anyone can view a public GitHub repository, but only you can push changes unless you grant collaborators access.

The deployed SQLite database uses the app's local filesystem and may not persist across redeployments or platform restarts. For durable multi-user hosting, configure a managed database before relying on stored accounts or user data.

## Tests

```powershell
python -m pytest tests/test_migrationmatch.py -q
```
