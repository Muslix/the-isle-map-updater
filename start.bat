@echo off 
echo 🗺️ Isle Map Updater 
echo ================== 
echo. 
echo Starting program... 
python isle_map_updater.py 
if %errorlevel% neq 0 ( 
    echo. 
    echo ❌ Error starting program! 
    echo Make sure you ran install.bat first 
    echo. 
    pause 
) 
