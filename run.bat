@echo off
echo 🦅 Starting DataHawk...
echo.

REM Check if virtual environment exists
if exist "ai\Scripts\activate.bat" (
    echo Activating virtual environment...
    call ai\Scripts\activate.bat
)

REM Check if dependencies are installed
python -c "import streamlit" 2>nul
if errorlevel 1 (
    echo Installing dependencies...
    python setup.py
    echo.
)

echo Starting DataHawk web interface...
echo Open your browser to: http://localhost:8501
echo.
streamlit run main.py

pause
