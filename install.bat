@echo off
REM Proje için gerekli Python kütüphanelerini yükleyin
echo Installing required Python packages...
pip install -r requirements.txt

REM Gerekli Python sürümünün kurulu olup olmadığını kontrol edin
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed. Please install Python before running this script.
    pause
    exit /b
)

echo Installation complete!
pause
