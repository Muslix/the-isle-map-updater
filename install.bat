@echo off 
echo 📦 Installing Isle Map Updater Dependencies 
echo =========================================== 
echo. 

echo 🔍 Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found! Installing Python...
    echo Please download and install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    echo After installing Python, run this script again.
    pause
    exit /b 1
)

echo 🔍 Checking for pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found! Installing pip...
    python -m ensurepip --upgrade
    if %errorlevel% neq 0 (
        echo ❌ pip installation failed!
        echo Please install pip manually
        pause
        exit /b 1
    )
)

echo Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies!
    pause
    exit /b 1
)

echo.
echo 🌐 Downloading ChromeDriver 138...
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager(driver_version='138.0.6907.99').install()"
if %errorlevel% equ 0 ( 
    echo. 
    echo ✅ Installation successful! 
    echo Now you can run start.bat 
) else ( 
    echo. 
    echo ❌ ChromeDriver installation failed! 
    echo Please check your internet connection
) 
echo. 
pause 