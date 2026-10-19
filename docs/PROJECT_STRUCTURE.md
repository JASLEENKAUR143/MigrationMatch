# Project structure

MigrationMatch keeps its application code separated by responsibility:

- `app.py` initializes Streamlit, loads the dataset, and routes pages.
- `analysis/` contains CSV loading, validation, and cleaning functions.
- `data/` contains the dataset generator, committed source CSV, and SQLite persistence layer. The local `.db` file is ignored by Git.
- `model/` contains feature engineering, recommendations, and machine-learning functionality.
- `ui/` contains reusable interface components and styles, session handling, navigation, and feature pages in `ui/pages/`.
- `assets/` is reserved for static interface assets.
- `tests/` contains automated tests.
- `.streamlit/config.toml` contains safe, non-secret Streamlit defaults. Deployment secrets belong in Streamlit's secret manager, never in Git.
- `PHP PROJECT/` is a separate project beside this application and is excluded from MigrationMatch version control.

The app and tests resolve the CSV relative to their source files. The database is stored beside the data module, so running Streamlit or tests does not require a particular shell working directory.
