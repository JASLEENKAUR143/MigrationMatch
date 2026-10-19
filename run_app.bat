@echo off
setlocal
cd /d "%~dp0"

set "PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%PYTHON%" (
    where py >nul 2>nul
    if not errorlevel 1 (
        py -3 -m venv ".venv"
    ) else (
        where python >nul 2>nul
        if errorlevel 1 (
            echo Python was not found. Install Python 3 and try again.
            pause
            exit /b 1
        )
        python -m venv ".venv"
    )
    if errorlevel 1 (
        echo Could not create the virtual environment.
        pause
        exit /b 1
    )
)

"%PYTHON%" -c "import streamlit, pandas, numpy, sklearn, plotly, matplotlib" >nul 2>nul
if errorlevel 1 (
    echo Installing project dependencies...
    "%PYTHON%" -m pip install -r "%~dp0requirements.txt"
    if errorlevel 1 (
        echo Dependency installation failed. Check your internet connection and try again.
        pause
        exit /b 1
    )
)

"%PYTHON%" -m streamlit run "%~dp0app.py" --server.headless false --server.port 8501
if errorlevel 1 (
    echo MigrationMatch stopped with an error.
    pause
    exit /b 1
)
